import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { CustomStrategy, MicroserviceOptions, Transport } from '@nestjs/microservices';
import { NatsJetStreamServer, NatsStreamConfig } from '@nestjs-plugins/nestjs-nats-jetstream-transport';
import { v4 as uuidv4 } from 'uuid';
import * as env from './constants';
import { DiscardPolicy, RetentionPolicy, StorageType } from 'nats';


let r = (Math.random() + 1).toString(36).substring(7);
async function bootstrap() {
  const streamConfig: NatsStreamConfig = {
    name: 'events',
    subjects: [ "metrics.url.*", "events.url*"],
    storage: StorageType.File,
    discard: DiscardPolicy.Old,
    retention: RetentionPolicy.Workqueue,
  };
  
  const options: CustomStrategy = {
    strategy: new NatsJetStreamServer({
      connectionOptions: {
        name: 'events-listener'+r,
        servers:env.NATS_SERVERS,
      },
      consumerOptions: {
        deliverTo: "listener." + uuidv4(),
        durable: 'listener-durable',
        deliverGroup: 'events-group',
        manualAck: true,
      },
      streamConfig
    }),
  };

  const app = await NestFactory.create(AppModule);
  
  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.REDIS,
    options: {
      host: env.REDIS_HOST,
      password: env.REDIS_PASSWORD
    },
  });
  await app.startAllMicroservices();
  const microService = app.connectMicroservice(options);
  await app.listen(env.APP_PORT);
  await microService.listen();
  console.log('Runing app');
}

bootstrap();





