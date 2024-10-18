import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'salaryView',
})
export class SalaryViewPipe implements PipeTransform {
  private defaultValue = 'N/A';

  transform(salary: number) {
    return typeof salary === 'number' ? salary : this.defaultValue;
  }
}
