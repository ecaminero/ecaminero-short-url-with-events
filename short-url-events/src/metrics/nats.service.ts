import { Injectable, Logger } from '@nestjs/common';
import { NatsJetStreamClientProxy } from '@nestjs-plugins/nestjs-nats-jetstream-transport';
import * as env from '../constants';

@Injectable()
export class NatsService {
  private readonly logger = new Logger(NatsService.name);
  constructor(private client: NatsJetStreamClientProxy) { }

  createMetrics(payload: object): void {
    this.client.emit<any>(env.NATS_METRICS_VISIT_CREATE, payload)
      .subscribe((pubAck) => {
        this.logger.log(`pubAck::received:: ${JSON.stringify(pubAck)}`);
      });
  }


}