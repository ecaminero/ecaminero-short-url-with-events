import { Module } from '@nestjs/common';
import { EventsModule } from './events/events.module';
import { RedisModule } from './redis/redis.module';
import { HttpModule } from '@nestjs/axios';
import { EventEmitterModule } from '@nestjs/event-emitter';

@Module({
  imports: [
    EventEmitterModule.forRoot(),
    HttpModule.registerAsync({
      useFactory: () => ({
        timeout: 5000,
        maxRedirects: 5,
      }),
    }),
    EventsModule,
    RedisModule,
  ],
})
export class AppModule {}