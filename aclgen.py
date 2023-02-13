from ipaddress import ip_network
import argparse

def network_convert(address):
    net = ip_network(address, strict=False)
    return f"{str(net.network_address)} {str(net.hostmask)}"

def tempalte_generater(address=None, port=None):
    if port:
        if '-' in port:
            range = "range"
            port = port.replace("-"," ")
        else:
            range = "eq"
    if address and port:
        return "{{flow}} {address} {{flow}}-port {range} {port}".format(address=network_convert(address), range=range, port=port)
    elif address:
        return "{{flow}} {address}".format(address=network_convert(address))
    elif port: 
        return "{{flow}}-port {range} {port}".format(range=range, port=port)

def args_processor(args):
    if not args.src and not args.dst:
        print("please input the -src or -dst argument\nyou can input -h to get help message")
        return
    if args.srcp or args.dstp:
        args.proto = 'tcp'
    args.src = args.src.split(',') if args.src else []
    args.dst = args.dst.split(',') if args.dst else []
    args.srcp = args.srcp.split(',') if args.srcp else []
    args.dstp = args.dstp.split(',') if args.dstp else []
    return args

def acl_generater(args):
    if args.src and args.dst:
        if args.srcp and args.dstp:
            for src in args.src:
                for dst in args.dst:
                    for src_port in args.srcp:
                        for dst_port in args.dstp:
                            yield (tempalte_generater(address=src, port=src_port),
                                   tempalte_generater(address=dst, port=dst_port),)
        elif args.srcp:
            for src in args.src:
                for dst in args.dst:
                    for src_port in args.srcp:
                        yield (tempalte_generater(address=src, port=src_port),
                               tempalte_generater(address=dst))
        elif args.dstp:
            for src in args.src:
                for dst in args.dst:
                    for dst_port in args.dstp:
                        yield (tempalte_generater(address=src),
                               tempalte_generater(address=dst, port=dst_port))
        else:
            for src in args.src:
                for dst in args.dst:
                    yield (tempalte_generater(address=src),
                           tempalte_generater(address=dst))
    elif args.src:
        if args.srcp and args.dstp:
            for src in args.src:
                for src_port in args.srcp:
                    for dst_port in args.dstp:
                        yield (tempalte_generater(address=src, port=src_port),
                               tempalte_generater(port=dst_port))
        elif args.srcp:
            for src in args.src:
                for src_port in args.srcp:
                    yield (tempalte_generater(address=src, port=src_port), None)
        elif args.dstp:
            for src in args.src:
                for dst_port in args.dstp:
                    yield (tempalte_generater(address=src),
                           tempalte_generater(port=dst_port))
        else:
            for src in args.src:
                yield (tempalte_generater(address=src), None)
    elif args.dst:
        if args.srcp and args.dstp:
            for dst in args.dst:
                for src_port in args.srcp:
                    for dst_port in args.dstp:
                        yield (tempalte_generater(port=src_port),
                               tempalte_generater(address=dst, port=dst_port))
        elif args.srcp:
            for dst in args.dst:
                for src_port in args.srcp:
                    yield (tempalte_generater(port=src_port),
                           tempalte_generater(address=dst))
        elif args.dstp:
            for dst in args.dst:
                for dst_port in args.dstp:
                    yield (None, tempalte_generater(address=dst, port=dst_port))
        else:
            for dst in args.dst:
                yield (None, tempalte_generater(address=dst))

def direction_controller(rule_number, action, proto, reverse,
          source_template, destination_template):
    if reverse:
        source = source_template.format(flow='destination') if source_template else "\b"
        destination = destination_template.format(flow='source') if destination_template else "\b"
        return f"rule {rule_number} {action} {proto} {destination} {source}"
    else:
        source = source_template.format(flow='source') if source_template else "\b"
        destination = destination_template.format(flow='destination') if destination_template else "\b"
        return f"rule {rule_number} {action} {proto} {source} {destination}"

def args_manager():
    parser = argparse.ArgumentParser(description='ACL generater')
    parser.add_argument('-src', help='源地址, 必选参数')
    parser.add_argument('-dst', help='目的地址, 必选参数')
    parser.add_argument('-srcp', help='源端口, 可选参数')
    parser.add_argument('-dstp', help='目的端口, 可选参数')
    parser.add_argument('-start', type=int, help='规则号起始数, 可选参数, 默认为0', default=0)
    parser.add_argument('-proto', help='协议, 可选参数: ip/tcp/udp', default='ip')
    parser.add_argument('-action', help='行为, 可选参数: permit/deny, 默认为permit', default='permit')
    parser.add_argument('--reverse', help='生成反向ACL', action="store_true")
    args = parser.parse_args()
    return args

def main():
    args = args_manager()
    args = args_processor(args)
    if args:
        for template in acl_generater(args):
            result = direction_controller(args.start, args.action, args.proto, args.reverse, *template)
            args.start += 1
            print(result)

if __name__ == "__main__":
    main()
