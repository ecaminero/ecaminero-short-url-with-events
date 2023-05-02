import { Controller, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Ctx, EventPattern, Payload } from '@nestjs/microservices';
import { MetricsService } from './metrics.service';
import { sleep } from '../utils';
import { Metrics } from './metrics.entity';
import { NatsJetStreamContext } from '@nestjs-plugins/nestjs-nats-jetstream-transport';
import { NatsService } from './nats.service';
import * as env from '../constants';


@Controller()
export class MetricsController {
  private readonly logger = new Logger(MetricsController.name);

  constructor(
    @InjectRepository(Metrics)
    private readonly metricsService: MetricsService,
    private readonly natsService: NatsService,
    ) { }

  @EventPattern(env.NATS_METRICS_VISIT_CREATE)
  async createMetrics(@Payload() data: any, @Ctx() context: NatsJetStreamContext) {
    context.message.ack();
    this.logger.log(`Subject:: ${context.message.subject} ::received`);
    this.logger.verbose(`Data:: ${JSON.stringify(data)}`);

    try {
      const result = await this.metricsService.save(data);
    } catch (error) {
      this.logger.error(error);
      await sleep(3000);
      this.logger.verbose("publishing to NATS");
      this.natsService.createMetrics(data);
    }
  }

}


