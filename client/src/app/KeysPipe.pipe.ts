import { PipeTransform, Pipe } from '@angular/core';

@Pipe({name: 'keys'})
export class KeysPipe implements PipeTransform {
  transform(value, args:string[]) : any {
    let keys = [];

    Object.keys(value).forEach(key => {
      keys.push(key)
    });

    return keys;
  }
}
