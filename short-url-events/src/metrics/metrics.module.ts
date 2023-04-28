
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { MetricsService } from './metrics.service';
import { MetricsController } from './metrics.controller';

import { Metrics } from './metrics.entity';
import { ClientsModule, Transport } from '@nestjs/microservices';
import * as env from '../constants';
import { group } from 'console';


@Module({
  imports: [
    ClientsModule.register([
      {name: 'NATS_METRICS', transport: Transport.NATS,
      options: { servers: env.NATS_SERVERS, queue: 'metrics', group: 'metrics'}}
    ]),
    TypeOrmModule.forFeature([Metrics]),
  ],
  providers: [MetricsService],
  controllers: [MetricsController],
})

export class MetricsModule { }