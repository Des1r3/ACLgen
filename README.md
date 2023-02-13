## ACLgen

### 快速生成 ACL 语句

### 使用方法
```bash
$ aclgen -h

usage: aclgen [-h] [-src SRC] [-dst DST] [-srcp SRCP] [-dstp DSTP] [-start START] [-proto PROTO] [-action ACTION][--reverse]

ACL generater

options:
-h, --help      show this help message and exit
-src SRC        源地址, 必选参数
-dst DST        目的地址, 必选参数
-srcp SRCP      源端口, 可选参数
-dstp DSTP      目的端口, 可选参数
-start START    规则号起始数, 可选参数, 默认为0
-proto PROTO    协议, 可选参数: ip/tcp/udp
-action ACTION  行为, 可选参数: permit/deny, 默认为permit
--reverse       生成反向ACL
```

### 使用参考
```bash
$ aclgen -src 172.16.2.1 -dst 172.16.1.1 -dstp 80,8080
rule 0 permit tcp source 172.16.2.1 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 80
rule 1 permit tcp source 172.16.2.1 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 8080
```

```bash
$ aclgen \
-src 172.16.2.1,172.16.2.2,192.168.1.0/24,192.168.2.0/24 \
-dst 172.16.1.1 \
-dstp 80,8080,8081,30010-30050

rule 0 permit tcp source 172.16.2.1 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 80
rule 1 permit tcp source 172.16.2.1 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 8080
rule 2 permit tcp source 172.16.2.1 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 8081
rule 3 permit tcp source 172.16.2.1 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port range 30010 30050
rule 4 permit tcp source 172.16.2.2 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 80
rule 5 permit tcp source 172.16.2.2 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 8080
rule 6 permit tcp source 172.16.2.2 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port eq 8081
rule 7 permit tcp source 172.16.2.2 0.0.0.0 destination 172.16.1.1 0.0.0.0 destination-port range 30010 30050
rule 8 permit tcp source 192.168.1.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port eq 80
rule 9 permit tcp source 192.168.1.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port eq 8080
rule 10 permit tcp source 192.168.1.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port eq 8081
rule 11 permit tcp source 192.168.1.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port range 30010 30050
rule 12 permit tcp source 192.168.2.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port eq 80
rule 13 permit tcp source 192.168.2.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port eq 8080
rule 14 permit tcp source 192.168.2.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port eq 8081
rule 15 permit tcp source 192.168.2.0 0.0.0.255 destination 172.16.1.1 0.0.0.0 destination-port range 30010 30050
```

---
目前暂时只支持 华为、华三 的设备