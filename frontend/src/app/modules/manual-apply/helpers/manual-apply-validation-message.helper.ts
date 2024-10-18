export class ManualApplyMessageHelper {
  static readonly ROOT_MESSAGE: string = 'You can\'t apply for the job:';
  static readonly EDUCATION_MESSAGE: string = ' Education does not match';
  static readonly CLEARANCE_MESSAGE: string = ' Clearance does not match';
  static readonly NEW_LINE: string = '\n';
  static readonly SUCCESS_MESSAGE: string = 'Your application has been sent';
  message: string;

  static getInitialMessage() {
    return ManualApplyMessageHelper.ROOT_MESSAGE +
      ManualApplyMessageHelper.NEW_LINE;
  }

  static addEducationError(): string {
    return ManualApplyMessageHelper.EDUCATION_MESSAGE +
      ManualApplyMessageHelper.NEW_LINE;
  }

  static addClearanceError(): string {
    return ManualApplyMessageHelper.CLEARANCE_MESSAGE +
      ManualApplyMessageHelper.NEW_LINE;
  }
}
