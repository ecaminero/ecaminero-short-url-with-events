
import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { EventsController } from './events.controller';
import { NATS_SERVERS } from '../constants';
import { EventService } from './events.service';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [
    HttpModule,
    ClientsModule.register([
      {
      name: 'NATS', transport: Transport.NATS,
      options: { 
        servers: NATS_SERVERS,
        queue: 'url_queue',
      }
    },
    ]),
  ],
  controllers: [EventsController],
  providers: [
    EventService
  ]
})

export class EventsModule {}