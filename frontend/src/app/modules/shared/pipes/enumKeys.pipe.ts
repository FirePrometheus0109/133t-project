import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'enumKeys'
})
export class EnumKeysPipe implements PipeTransform {
  transform(data: Object) {
    return Object.keys(data);
  }
}
