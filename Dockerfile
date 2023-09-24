FROM python:3.9-alpine

RUN mkdir -p /ctf
COPY ctf.py /ctf
COPY .env /ctf
WORKDIR /ctf

RUN pip install discord.py python-dotenv
RUN addgroup -S ctf && adduser -S ctf -G ctf
RUN chown -R ctf:ctf /ctf

USER ctf

CMD ["python", "./ctf.py"]
