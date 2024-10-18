import { Pipe, PipeTransform } from '@angular/core';

export const firstMemberInKeys = 'all';


@Pipe({
  name: 'keys'
})
export class KeysPipe implements PipeTransform {
  transform(value, args: string[]): any {
    const keys = [];
    for (const enumMember in value) {
      if (value.hasOwnProperty(enumMember)) {
        (enumMember === firstMemberInKeys)
          ? keys.splice(0, 0, {key: enumMember, value: value[enumMember]})
          : keys.push({key: enumMember, value: value[enumMember]});
      }
    }
    return keys;
  }
}
