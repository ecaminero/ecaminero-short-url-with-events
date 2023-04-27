
import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { EventEmitterModule } from '@nestjs/event-emitter';
import { RedisController } from './redis.controller';
import { REDIS_HOST, REDIS_PASSWORD, REDIS_PORT } from '../constants';
import { NATS_SERVERS } from '../constants';

@Module({
  imports: [
    EventEmitterModule.forRoot(),
    ClientsModule.register([
      {
        name: 'NATS', transport: Transport.NATS,
        options: { servers: NATS_SERVERS }
      },
      {
        name: 'REDIS', transport: Transport.REDIS,
        options: {
          host: REDIS_HOST,
          password: REDIS_PASSWORD
        },
      },
    ]),
  ],
  controllers: [RedisController],
})

export class RedisModule { }