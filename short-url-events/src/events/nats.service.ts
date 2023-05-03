import { Injectable, Logger } from '@nestjs/common';
import { NatsJetStreamClientProxy } from '@nestjs-plugins/nestjs-nats-jetstream-transport';
import * as env from '../constants';

@Injectable()
export class NatsService {
  private readonly logger = new Logger(NatsService.name);
  constructor(private client: NatsJetStreamClientProxy) { }

  deleteKey(payload: object): void {
    this.client.emit<any>(env.NATS_EVENT_URL_DELETE, payload)
      .subscribe((pubAck) => {
        this.logger.log(`pubAck::received:: ${JSON.stringify(pubAck)}`);

      });
  }


}