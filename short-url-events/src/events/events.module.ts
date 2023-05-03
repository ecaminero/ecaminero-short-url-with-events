
import { Module } from '@nestjs/common';
import { EventsController } from './events.controller';
import { EventService } from './events.service';
import { NatsService } from './nats.service';

import { HttpModule } from '@nestjs/axios';
import { NatsJetStreamTransport } from '@nestjs-plugins/nestjs-nats-jetstream-transport';
import * as env from '../constants';


@Module({
  imports: [
    HttpModule.register({
      timeout: 2000,
      maxRedirects: 1,
    }),
    NatsJetStreamTransport.register({
      connectionOptions: {
        servers: env.NATS_SERVERS,
        name: 'events',
      },
    }),
  ],
  exports: [NatsService],
  controllers: [EventsController],
  providers: [EventService, NatsService]
})

export class EventsModule {}