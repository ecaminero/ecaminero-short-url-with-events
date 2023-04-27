import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ClientsModule, MicroserviceOptions, Transport } from '@nestjs/microservices';
import * as env from './constants';


async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.NATS,
    options: { servers: env.NATS_SERVERS, retryDelay: 3000 },
  });
  
  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.REDIS,
    options: {
      host: env.REDIS_HOST,
      password: env.REDIS_PASSWORD
    },
  });
  await app.startAllMicroservices();
  await app.listen(env.APP_PORT);
  console.log('Runing app');
}

bootstrap();





