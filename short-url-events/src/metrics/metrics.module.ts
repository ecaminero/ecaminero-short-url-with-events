
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { MetricsService } from './metrics.service';
import { MetricsController } from './metrics.controller';
import { NatsService } from './nats.service';

import { Metrics } from './metrics.entity';
import { NatsJetStreamTransport } from '@nestjs-plugins/nestjs-nats-jetstream-transport';

import * as env from '../constants';

@Module({
  imports: [
    TypeOrmModule.forFeature([Metrics]),
    NatsJetStreamTransport.register({
      connectionOptions: {
        servers: env.NATS_SERVERS,
        name: 'metrics',
      },
    }),
  ],
  providers: [MetricsService, NatsService],
  controllers: [MetricsController],
})

export class MetricsModule { }



