FROM redis:5.0.4-alpine

RUN apk add curl bash

ENV REDIS_HOSTNAME=redis
RUN mkdir /workgroup
COPY ./worker.sh /workgroup/worker.sh
RUN chmod +x /workgroup/worker.sh

CMD ["/workgroup/worker.sh"]
