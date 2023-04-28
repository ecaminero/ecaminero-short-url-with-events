import { Controller, Inject, Logger } from '@nestjs/common';
import { ClientProxy, Ctx, MessagePattern, NatsContext, Payload } from '@nestjs/microservices';
import { EventService } from './events.service';
import { sleep } from '../utils';
import * as cons from '../constants';

@Controller()
export class EventsController {
  private readonly logger = new Logger(EventService.name);

  constructor(
    @Inject('NATS') private client: ClientProxy,
    private readonly eventService: EventService) {}

  @MessagePattern(cons.NATS_CREATE_URL)
  async getNotifications(@Payload() data: any, @Ctx() context: NatsContext){
    this.logger.log(`Subject:: ${context.getSubject()}`);
    this.logger.verbose(JSON.stringify(data));
  }

  @MessagePattern(cons.NATS_EXPIRED_URL)
  async expired(@Payload() data: any, @Ctx() context: NatsContext){
    this.logger.log(`Subject:: ${context.getSubject()}:: ${data}`);
    this.logger.verbose(JSON.stringify(data));
    try {
      const results = await this.eventService.getFromQuery({ query: `key=${data}` })
      for (const url of results) {
        const result = await this.eventService.delete(url["id"])
        this.logger.log(`delete:: ${result["id"]}`);
      }
    } catch (error) {
      this.logger.error(error);
      this.logger.verbose("publishing to NATS");
      sleep(3000);
      this.client.send(cons.NATS_EXPIRED_URL, data).subscribe();
    }
  }
  
}
