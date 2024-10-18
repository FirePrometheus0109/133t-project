import {JobSeekerModule} from './job-seeker.module';

describe('JobSeekerModule', () => {
  let jobSeekerModule: JobSeekerModule;

  beforeEach(() => {
    jobSeekerModule = new JobSeekerModule();
  });

  it('should create an instance', () => {
    expect(jobSeekerModule).toBeTruthy();
  });
});
