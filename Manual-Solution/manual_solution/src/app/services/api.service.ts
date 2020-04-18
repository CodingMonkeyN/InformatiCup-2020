import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Response } from '../models/response';
import { Observable } from 'rxjs';
interface parse { success: boolean }
@Injectable({
  providedIn: 'root'
})



export class ApiService {
  serverUrl = 'http://192.168.0.192:8000';
  infoAPIUrl = 'http://localhost:50123';

  constructor(private http: HttpClient) {

  }

  getRoundData() {
    return this.http.get<any>(this.serverUrl + '/frontend');
  }

  sendAction(action): Observable<parse> {
    return this.http.post<parse>(this.serverUrl + '/frontend', action);
  }

  startGame(): Observable<parse> {
    var d = this.http.get<parse>(this.serverUrl + '/game');
    return d;
  }

  getExtradedGameInfo(gameObj) : any{
    return this.http.post(this.infoAPIUrl + '/game_info', gameObj);
  }

  getAIAction(gameObj){
    return this.http.post<any>(this.infoAPIUrl, gameObj);
  }

  getStrategy(){
    return this.http.get<any>(this.infoAPIUrl + '/strategy');
  }


}
