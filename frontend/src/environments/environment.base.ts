export const minYearAvailableForSelection = 1956;
export const environment = {
  production: false,
  baseUrl: 'http://localhost:8000',
  apiPrefix: 'api',
  apiVersion: 'v1',
  jspMinPublishSkillsCount: 3,
  maxSkillsCount: 20,
  maxQuestionsLength: 10,
  maxCoverLettersCount: 5,
  maxInvitedUsersCount: 10,
  maxExperienceCount: 10,
  maxEducationCount: 30,
  maxLetterTemplatesCount: 100,
  searchDebounceTime: 250,
  snackBarDelay: 5000,
  minimalLengthOfSearchStr: 2,
  maxAssignedUser: 50,
  quickViewLimit: 1,
  reportGraphDateLength: 4,
  newestJobsParamsOnDashboard: {limit: 3, ordering: '-modified_at'},
  savedJobsLimitOnDashboard: 5,
  // TODO: remove OTHER_REASON when backend implements it in deletion reasons (declared in UPPER_SNAKE_CASE to attract attention)
  OTHER_REASON: 'Other reason',
  userAccountIsDisabled: 'User account is disabled.',
  showTechnicalInfo: true,
  expiredSubscriptionResponse: 'You can not perform this action without subscription.',
  deletedCompanyUserResponse: 'There is deleted user with certain email in company.',
  actionToRestore: 'RESTORE_STATUS',
  maxCommentTitleInputLength: 128,
  maxCommentBodyInputLength: 2048,
  dateChoiceMin: new Date(minYearAvailableForSelection, 0, 1),
  trialLengthPeriod: 17,
  shortNotificationsInterval: {dueTime: 0, period: 60000},
  minTimeBeforeTokenWillBeExpiredWithoutRefresh: 28800 // -> 8h
};
