
import { Events } from './events';
import { Cities } from './cities';

export class Response {
    cities: Cities[];
    events: Events[];
    outcome: string;
    points: number;
    round: number;

}