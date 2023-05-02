import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { catchError, lastValueFrom, map, firstValueFrom } from 'rxjs';
import { URL_SHORT_URL_APP } from 'src/constants';
import { AxiosError } from 'axios';


@Injectable()
export class EventService {
  private serviceUrl = `${URL_SHORT_URL_APP}/admin`;
  private readonly logger = new Logger(EventService.name);

  constructor(private readonly httpService: HttpService) { }

    async getFromQuery({ query }: { query: string; }):  Promise<object[]>{
    const url = `${this.serviceUrl}/url?${query}`;
    const { data } = await firstValueFrom(
      this.httpService.get<object[]>(url).pipe(
        catchError((error: AxiosError) => {
          this.logger.error(error.response.data);
          throw error;
        }),
      ),
    );

    return data;
  }

  delete(id: string): Promise<object[]> {
    const url = `${this.serviceUrl}/url/${id}`;
    console.log(url)
    const data = lastValueFrom(
      this.httpService.delete<object[]>(url).pipe(
        map((res) => {return res.data}),
        catchError((error: AxiosError) => {
          this.logger.error(error);
          throw error;
        }),
      ),
    );
    return data
  }

}