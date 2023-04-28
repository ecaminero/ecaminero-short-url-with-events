import { Controller, Inject, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { ClientProxy, Ctx, MessagePattern,EventPattern, NatsContext, Payload } from '@nestjs/microservices';
import { MetricsService } from './metrics.service';
import { sleep } from '../utils';
import { Metrics } from './metrics.entity';
import * as env from '../constants';
import { group } from 'console';

@Controller()
export class MetricsController {
  private readonly logger = new Logger(MetricsController.name);

  constructor(
    @Inject('NATS_METRICS') private client: ClientProxy,
    @InjectRepository(Metrics)
    private readonly metricsService: MetricsService) { }

  @MessagePattern(env.NATS_METRICS_VISIT_CREATE)
  async createMetrics(@Payload() data: any, @Ctx() context: NatsContext) {
    let result = {}
    this.logger.log(`Subject:: ${context.getSubject()}`);
    this.logger.verbose(`Data:: ${JSON.stringify(data)}`);
    try {
     result = await this.metricsService.save(data);
    } catch (error) {
      console.log("////////////////////////////////")
    }
    console.log(Reflect.has(result, "id"))
    
    if (Reflect.has(result, "id")) {
      return result;
    } else {
      this.logger.error(result);
      this.logger.verbose("Posting on nats");
      this.client.send(env.NATS_METRICS_VISIT_CREATE, data).subscribe();
    }
  }
}


