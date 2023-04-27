import { Controller, Inject, Logger } from '@nestjs/common';
import { ClientProxy, MessagePattern, Payload } from '@nestjs/microservices';
import {REDIS_EXPIRED_KEY, NATS_EXPIRED_URL } from '../constants';

@Controller()
export class RedisController {
  private readonly logger = new Logger(RedisController.name);

  constructor(@Inject('NATS') private client: ClientProxy) {}

  @MessagePattern(REDIS_EXPIRED_KEY)
  getNotifications(@Payload() data: any){
    this.logger.log(`Event: ${NATS_EXPIRED_URL}:: ${data}`);
    this.client.send(NATS_EXPIRED_URL, data).subscribe();
  }
}
