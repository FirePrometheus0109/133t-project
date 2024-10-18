import { formatDate } from '@angular/common';
import * as moment from 'moment';
import { environment } from 'src/environments/environment.base';
import { DateBasis } from '../../shared/enums/company-reports.enums';


export class DateTimeHelper {
  static isFuture(time: Date) {
    return moment(time).isAfter();
  }

  static firstDayOfSubscription(time: Date) {
    return moment(time).format('DD MMMM');
  }

  static getGraphFirstDate(to_date: Date, basis: DateBasis): Date {
    const graphLength = environment.reportGraphDateLength;

    switch (basis) {
      case(DateBasis.DAY):
        return moment(to_date).subtract(graphLength, 'd').toDate();
      case(DateBasis.MONTH):
        return moment(to_date).subtract(graphLength, 'M').toDate();
      case(DateBasis.WEEK):
        return moment(to_date).subtract(graphLength, 'w').toDate();
      default:
        return moment(to_date).subtract(graphLength, 'd').toDate();
    }
  }

  static formatGraphDate(date: Date, basis: DateBasis) {
    switch (basis) {
      case(DateBasis.DAY):
        return moment(date).format('MMM Do');
      case(DateBasis.MONTH):
        return moment(date).format('MMMM');
      case(DateBasis.WEEK):
        return `${moment(date).format('MMM Do')} - ${moment(date).add(1, 'w').format('MMM Do')}`;
      default:
        return moment(date).format('MMM Do');
    }
  }

  static enumerateDaysBetweenDates(startDate, endDate) {
    return DateTimeHelper.enumerateBetweenDates(arguments, 'day', 'd');
  }

  static enumerateWeeksBetweenDates(startDate, endDate) {
    return DateTimeHelper.enumerateBetweenDates(arguments, 'isoWeek', 'w');
  }

  static enumerateMonthBetweenDates(startDate, endDate) {
    return DateTimeHelper.enumerateBetweenDates(arguments, 'month', 'M');
  }

  static enumerateBetweenDates(args, unitOfTime, unitOfPeriod) {
    const dates = [];

    const currDate = moment(args[0]).utc().startOf(unitOfTime);
    const lastDate = moment(args[1]).utc().startOf(unitOfTime);

    while (currDate.add(1, unitOfPeriod).diff(lastDate) <= 0) {
      dates.push(currDate.clone().toJSON());
    }
    return dates;
  }

  static isDateEqual(firstDate, secondDate) {
    return moment(firstDate).isSame(secondDate, 'day');
  }

  static compareDate(firstDate, secondDate) {
    return moment(firstDate.name).diff(moment(secondDate.name));
  }

  static isDateExpired(limitDate) {
    return moment().isAfter(limitDate);
  }

  static getDate(date: string) {
    return formatDate(date, 'MM/dd/yyyy', 'en-US');
  }

  static getDateWithTime(date: string) {
    return formatDate(date, 'MM/dd/yyyy, h:mm a', 'en-US');
  }
}
