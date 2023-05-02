import { InjectRepository } from '@nestjs/typeorm';
import { Injectable, Logger, Inject } from '@nestjs/common';
import { Metrics } from './metrics.entity'
import { Repository } from 'typeorm';
import { ErrorType } from '../types';


@Injectable()
export class MetricsService {
  private readonly logger = new Logger(MetricsService.name);

  constructor(
    @InjectRepository(Metrics)
    private readonly metricsRepository: Repository<Metrics>,
  ) { }

  async save(data: object): Promise<ErrorType | Metrics> {
    try {
      const metrics = this.metricsRepository.create(data);
      this.logger.log(`Create metrics: ${JSON.stringify(metrics)}`);
      return await this.metricsRepository.save(metrics);
    } catch (error) {
      this.logger.error(`Error: ${error.message}`);
      throw error;
    }
  }

}

