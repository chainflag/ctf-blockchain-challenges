FROM ubuntu:18.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python3 python3-pip xinetd vim

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome web3 py-solc-x
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple sty
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple tqdm
RUN pip3 install colorfulpanda==0.4

#RUN python3 -m solcx.install v0.5.10
#RUN python3 -m solcx.install v0.6.6

RUN mkdir /root/ethbot

COPY ./ethbot /root/ethbot
COPY ./start.sh /start.sh
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./solc-v0.5.10 /root/.solcx/solc-v0.5.10
COPY ./solc-v0.6.6 /root/.solcx/solc-v0.6.6

RUN chmod +x /start.sh

CMD ["/start.sh"]

EXPOSE 10001
