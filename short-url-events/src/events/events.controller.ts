import { Controller, Logger } from '@nestjs/common';
import { Ctx, MessagePattern, Payload, RedisContext } from '@nestjs/microservices';
import { NatsJetStreamContext } from '@nestjs-plugins/nestjs-nats-jetstream-transport';
import { EventService } from './events.service';
import { NatsService } from './nats.service';
import { sleep } from '../utils';
import * as env from '../constants';
import { v4 as uuidv4 } from 'uuid';


@Controller()
export class EventsController {
  private readonly logger = new Logger(EventService.name);

  constructor(
    private readonly natsService: NatsService,
    private readonly eventService: EventService) {}

  @MessagePattern(env.NATS_EVENT_URL_CREATE)
  async getNotifications(@Payload() data: object, @Ctx() context: NatsJetStreamContext){
    this.logger.log(`Subject:: ${context.message.subject} ::received`);
    this.logger.verbose(JSON.stringify(data));
    context.message.ack();
  }

  @MessagePattern(env.NATS_EVENT_URL_DELETE)
  async deleteUrl(@Payload() data: object, @Ctx() context: NatsJetStreamContext){
    this.logger.log(`Subject:: ${context.message.subject} ::received`);
    this.logger.verbose(JSON.stringify(data));
    try {
      const results = await this.eventService.getFromQuery({ query: `key=${data["short_url"]}` });
      for (const url of results) {
        const result = await this.eventService.delete(url["id"])
        this.logger.log(`deleted:: ${result["id"]}`);
      }
      context.message.ack;
    } catch (error) {
      this.logger.error(error);
      await sleep(2000);
      this.logger.verbose("publishing to NATS");
      this.natsService.deleteKey(data);
    }
  }

  @MessagePattern(env.REDIS_EXPIRED_KEY)
  expiredKeyFromRedis(@Payload() data: string, @Ctx() context: RedisContext){
    this.logger.log(`Event: ${context.getChannel()}:: ${data}`);
    const payload = { eventId: uuidv4(), short_url: data}
    this.natsService.deleteKey(payload);
  }
  
}
