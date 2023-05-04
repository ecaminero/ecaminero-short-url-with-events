import { Module } from '@nestjs/common';
import { EventsModule } from './events/events.module';
import { MetricsModule } from './metrics/metrics.module';

import { HttpModule } from '@nestjs/axios';
import { TypeOrmModule } from '@nestjs/typeorm';

import * as env from './constants';

@Module({
  imports: [

    TypeOrmModule.forRoot({
      type: "postgres",
      host: env.DB_HOST,
      port: env.DB_PORT,
      username: env.DB_USERNAME,
      password: env.DB_PASSWORD,
      database: env.DB_DATABASE,
      synchronize: Boolean(env.DB_SYNC),
      autoLoadEntities: true,
    }),
    HttpModule.registerAsync({
      useFactory: () => ({
        timeout: 5000,
        maxRedirects: 5,
      }),
    }),
    EventsModule,
    MetricsModule
  ],
})
export class AppModule { }