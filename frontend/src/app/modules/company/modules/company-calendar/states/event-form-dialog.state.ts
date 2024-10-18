import { UpdateFormErrors, UpdateFormValue } from '@ngxs/form-plugin';
import { Action, Selector, State, StateContext, Store } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, concatMap, tap } from 'rxjs/operators';
import * as Url from 'url-parse';

import { FetchBasedState } from './fetch-based.state';

import { EventFormService } from '../services/event-form.service';

import { CoreActions } from '../../../../core/actions';
import { EventFormActions } from '../actions';

import { AuthState } from '../../../../auth/states/auth.state';

import { environment } from '../../../../../../environments/environment';
import { SnackBarMessageType } from '../../../../shared/models/snack-bar-message';


// TODO: move to model
export interface JobEnum {
  id: number;
  title: string;
}


export enum EventAttendeeStatus {
  INVITED = 'Invited',
  ACCEPTED = 'Accepted',
  REJECTED = 'Rejected'
}


export const companyEventFormKey = 'companyeventform';
export const companyEventFormStateKey = 'form';
export const eventStateKey = 'event';
export const jobsStateKey = 'jobs';
export const citiesStateKey = 'cities';
export const zipsStateKey = 'zips';
export const colleaguesStateKey = 'colleagues';
export const candidatesStateKey = 'candidates';
export const zonesStateKey = 'zones';
export const letterTemplatesStateKey = 'letter_templates';
export const countriesStateKey = 'countries';

export const companyEventFormStateFullKey = companyEventFormKey + '.' + companyEventFormStateKey;

const parseServerTimeZones = (timezones: object): any[] => {
  return Object.keys(timezones).map(key => {
    return {
      title: timezones[key],
      value: key
    };
  });
};

const parseServerRelatedUser = (user, onlyId = false) => {
  if (onlyId) {
    return user.user.id;
  }
  return {
    ...user,
    title: user.user.name,
    value: user.user.id
  };
};

const parseServerCandidate = (candidate, onlyId = false) => {
  const {job_seeker: {user}, ...restOfCandidate} = candidate;

  if (onlyId) {
    return user.id;
  }
  return {
    ...restOfCandidate,
    user: user,
    title: user.name,
    value: user.id
  };
};

const parseServerRelatedUserCollection = (collection: any[], onlyId = false, parser = parseServerRelatedUser) => {
  return collection.map(item => parser(item, onlyId));
};

const parseServerLetterTemplates = (letterTemplates: any[]) => {
  return letterTemplates.map(letterTemplate => {
    return {
      ...letterTemplate,
      title: letterTemplate.name
    };
  });
};

const parseServerCountry = (country, onlyId = false) => {
  if (onlyId) {
    return country.id;
  }
  return {
    ...country,
    title: country.name
  };
};

const parseServerCountries = (countries: any[]) => {
  return countries.map(country => parseServerCountry(country));
};

const parseServerCity = (city, onlyId = false) => {
  if (onlyId) {
    return city.id;
  }
  return {
    ...city,
    title: city.name + ', ' + city.state.name
  };
};

const parseServerCities = (cities: any[]) => {
  return cities.map(city => parseServerCity(city));
};

const parseServerZip = (zip, onlyId = false) => {
  if (onlyId) {
    return zip.id;
  }
  return {
    ...zip,
    title: zip.code
  };
};

const parseServerZips = (zips: any[]) => {
  return zips.map(zip => parseServerZip(zip));
};

const parseServerEvent = (event) => {
  return {
    ...event,
    location: {
      ...event.location,
      country: parseServerCountry(event.location.country, true),
      city: parseServerCity(event.location.city),
      zip: parseServerZip(event.location.zip, true)
    },
    colleagues: parseServerRelatedUserCollection(event.colleagues),
    candidates: parseServerRelatedUserCollection(event.candidates)
  };
};

const dumpEventToServerAcceptableData = (eventData) => {
  return {
    ...eventData,
    location: {
      ...eventData.location,
      city: parseServerCity(eventData.location.city, true)
    },
    colleagues: parseServerRelatedUserCollection(eventData.colleagues, true),
    candidates: parseServerRelatedUserCollection(eventData.candidates, true),
    job: eventData.job.id,
    type: eventData.type.id
  };
};


export interface EventFormStateModel {
  [companyEventFormStateKey]: {
    pending: boolean,
    model: any,
    dirty: boolean,
    status: string,
    errors: any
  };
  [eventStateKey]: {
    pending: boolean,
    data?: any,
    errors: any
  };
  [colleaguesStateKey]: {
    pending: boolean,
    data?: any[],
    errors: {}
  };
  [candidatesStateKey]: {
    pending: boolean,
    data?: any[],
    errors: any
  };
  [zonesStateKey]: {
    pending: boolean,
    data?: {[key: string]: string},
    errors: any
  };
  [jobsStateKey]: {
    pending: boolean,
    data?: JobEnum[],
    errors: any
  };
  [letterTemplatesStateKey]: {
    pending: boolean,
    data?: any[],
    errors: {}
  };
  [countriesStateKey]: {
    pending: boolean,
    data?: any,
    errors: {}
  };
  [citiesStateKey]: {
    pending: boolean,
    data?: any,
    errors: {}
  };
  [zipsStateKey]: {
    pending: boolean;
    data?: any,
    errors: {}
  };
}


export const defaultEventFormState: EventFormStateModel = {
  [companyEventFormStateKey]: {
    pending: false,
    model: undefined,
    dirty: false,
    status: '',
    errors: {}
  },
  [eventStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [colleaguesStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [candidatesStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [zonesStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [jobsStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [letterTemplatesStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [countriesStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [citiesStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
  [zipsStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  }
};


@State<EventFormStateModel>({
  name: companyEventFormKey,
  defaults: defaultEventFormState
})
export class EventFormState extends FetchBasedState {
  defaultState = defaultEventFormState;

  @Selector()
  static jobsState(state: EventFormStateModel) {
    return state[jobsStateKey];
  }

  @Selector()
  static citiesState(state: EventFormStateModel) {
    return state[citiesStateKey];
  }

  @Selector()
  static citiesList(state: EventFormStateModel) {
    return state[citiesStateKey].data ? state[citiesStateKey].data.results : [];
  }

  @Selector()
  static zipsState(state: EventFormStateModel) {
    return state[zipsStateKey];
  }

  @Selector()
  static colleaguesState(state: EventFormStateModel) {
    return state[colleaguesStateKey];
  }

  @Selector()
  static candidatesState(state: EventFormStateModel) {
    return state[candidatesStateKey];
  }

  @Selector()
  static zonesState(state: EventFormStateModel) {
    return state[zonesStateKey];
  }

  @Selector()
  static formState(state: EventFormStateModel) {
    return state.form;
  }

  @Selector()
  static eventState(state: EventFormStateModel) {
    return state[eventStateKey];
  }

  @Selector()
  static eventOwner(state: EventFormStateModel) {
    if (state[eventStateKey].data) {
      return state[eventStateKey].data.owner;
    }
    return {};
  }

  @Selector()
  static eventType(state: EventFormStateModel) {
    if (state.form.model) {
      return state.form.model.type;
    }
    else if (state[eventStateKey].data) {
      return state[eventStateKey].data.type;
    }
    return {};
  }

  @Selector()
  static letterTemplatesState(state: EventFormStateModel) {
    return state[letterTemplatesStateKey];
  }

  @Selector()
  static countriesState(state: EventFormStateModel) {
    return state[countriesStateKey];
  }

  constructor(private eventFormService: EventFormService, private store: Store) {
    super();
  }

  @Action(EventFormActions.LoadInitData)
  loadInitData(ctx: StateContext<EventFormStateModel>, {forEvent}: EventFormActions.LoadInitData) {
    if (forEvent.id) {
      ctx.dispatch(new EventFormActions.LoadEvent(forEvent.id));
    }
    else {
      const user = this.store.selectSnapshot(AuthState.user);
      ctx.dispatch(new UpdateFormValue({
        value: {
          colleagues: [
            {
              user: {id: user.pk},
              title: user.first_name + ' ' + user.last_name,
              value: user.pk,
              status: EventAttendeeStatus.ACCEPTED
            }
          ]
        },
        path: companyEventFormStateFullKey
      }));
    }
    ctx.dispatch(new EventFormActions.LoadColleagues());
    ctx.dispatch(new EventFormActions.LoadJobPostings());
    ctx.dispatch(new EventFormActions.LoadZones());
    ctx.dispatch(new EventFormActions.LoadLetterTemplates());
    ctx.dispatch(new EventFormActions.LoadCountries());
  }

  @Action(EventFormActions.CleenUp)
  cleenUp(ctx: StateContext<EventFormStateModel>) {
    ctx.setState(defaultEventFormState);
  }

  checkEventTime(ctx: StateContext<EventFormStateModel>) {
    const state = ctx.getState();
    const { model: { time_from, time_to } } = EventFormState.formState(state);
    const { data } = EventFormState.eventState(state);
    const eventId = data ? data.id : null;
    const queryParams: { time_from: string, time_to: string, id?: number } = { time_from, time_to };
    if (eventId) {
      queryParams.id = eventId;
    }
    return this.eventFormService.checkTime(queryParams)
      .pipe(
        catchError(error => {
          ctx.dispatch(new UpdateFormErrors({
            errors: {...error},
            path: companyEventFormStateFullKey
          }));
          return of(error);
        })
      );
  }

  createOrUpdateEvent(ctx: StateContext<EventFormStateModel>) {
    const state = ctx.getState();
    const eventData = EventFormState.eventState(state);
    const formData = EventFormState.formState(state);
    const serverAcceptableData = dumpEventToServerAcceptableData(formData.model);
    const id = eventData.data && eventData.data.id;
    this.setEntityPending(ctx, companyEventFormStateKey);
    if (id) {
      return this.eventFormService.updateEvent(id, serverAcceptableData)
        .pipe(
          tap(() => {
            ctx.dispatch(new EventFormActions.CloseEventFormDialog());
            this.setEntityPending(ctx, companyEventFormStateKey, false);
            ctx.dispatch(new CoreActions.SnackbarOpen({
              message: 'Event was successfully updated!',
              delay: environment.snackBarDelay,
              type: SnackBarMessageType.SUCCESS,
            }));
          }),
          catchError(error => {
            this.setEntityPending(ctx, companyEventFormStateKey, false);
            ctx.dispatch(new UpdateFormErrors({
              errors: { ...error.error },
              path: companyEventFormStateFullKey
            }));
            return of(error);
          })
        );
    }
    else {
      return this.eventFormService.createEvent(serverAcceptableData)
        .pipe(
          tap(() => {
            ctx.dispatch(new EventFormActions.CloseEventFormDialog());
            this.setEntityPending(ctx, companyEventFormStateKey, false);
            ctx.dispatch(new CoreActions.SnackbarOpen({
              message: 'Event was successfully created!',
              delay: environment.snackBarDelay,
              type: SnackBarMessageType.SUCCESS,
            }));
          }),
          catchError(error => {
            this.setEntityPending(ctx, companyEventFormStateKey, false);
            ctx.dispatch(new UpdateFormErrors({
              errors: { ...error.error },
              path: companyEventFormStateFullKey
            }));
            return of(error);
          })
        );
    }
  }

  @Action(EventFormActions.DeleteEvent)
  deleteEvent(ctx: StateContext<EventFormStateModel>) {
    const state = ctx.getState();
    const eventData = EventFormState.eventState(state);
    const id = eventData.data && eventData.data.id;
    if (!id) {
      return;
    }
    this.setEntityPending(ctx, companyEventFormStateKey);
    return this.eventFormService.deleteEvent(id)
      .pipe(
        tap(
          () => {
            ctx.dispatch(new EventFormActions.CloseEventFormDialog());
            this.setEntityPending(ctx, companyEventFormStateKey, false);
            ctx.dispatch(new CoreActions.SnackbarOpen({
              message: 'Event was deleted!',
              delay: environment.snackBarDelay,
              type: SnackBarMessageType.WARNING,
            }));
          }
        ),
        catchError(error => {
          this.setEntityPending(ctx, companyEventFormStateKey, false);
          return of(error);
        })
      );
  }

  @Action(EventFormActions.Submit)
  submit(ctx: StateContext<EventFormStateModel>, {force = false}: EventFormActions.Submit) {
    if (force) {
      return this.createOrUpdateEvent(ctx);
    }
    this.setEntityPending(ctx, companyEventFormStateKey);
    return this.checkEventTime(ctx)
      .pipe(
        concatMap(checkResult => {
          const { message } = checkResult;
          if (!message) {
            return this.createOrUpdateEvent(ctx);
          }
          this.setEntityPending(ctx, companyEventFormStateKey, false);
          return ctx.dispatch(new UpdateFormErrors({
            errors: { collision: message },
            path: companyEventFormStateFullKey
          }));
        })
      );
  }

  @Action(EventFormActions.LoadEvent)
  loadEvent(ctx: StateContext<EventFormStateModel>, {eventId}: EventFormActions.LoadEvent) {
    this.setEntityPending(ctx, eventStateKey);
    return this.eventFormService.getEvent(eventId)
      .pipe(
        tap(result => {
          const validEvent = parseServerEvent(result);
          this.setEntityLoadSuccess(ctx, eventStateKey, validEvent);
          ctx.dispatch(new UpdateFormValue({
            value: validEvent,
            path: companyEventFormStateFullKey
          }));
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, eventStateKey, error);
        })
      );
  }

  @Action(EventFormActions.LoadColleagues)
  loadColleagues(ctx: StateContext<EventFormStateModel>) {
    this.setEntityPending(ctx, colleaguesStateKey);
    return this.eventFormService.getColleagues()
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, colleaguesStateKey, parseServerRelatedUserCollection(result));
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, colleaguesStateKey, error);
        })
      );
  }

  @Action(EventFormActions.LoadCandidates)
  loadCandidates(ctx: StateContext<EventFormStateModel>, {jobId}: EventFormActions.LoadCandidates) {
    this.setEntityPending(ctx, candidatesStateKey);
    return this.eventFormService.getCandidates(jobId)
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, candidatesStateKey, parseServerRelatedUserCollection(result, false, parseServerCandidate));
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, candidatesStateKey, error);
        })
      );
  }

  @Action(EventFormActions.UpdateCandidates)
  updateCandidates(ctx: StateContext<EventFormStateModel>, {jobId}: EventFormActions.UpdateCandidates) {
    if (jobId) {
      ctx.dispatch(new EventFormActions.LoadCandidates(jobId));
    }
    else {
      this.setEntityLoadSuccess(ctx, candidatesStateKey, defaultEventFormState[candidatesStateKey].data);
    }
    ctx.dispatch(new UpdateFormValue({
      value: {
        candidates: []
      },
      path: companyEventFormStateFullKey
    }));
  }

  @Action(EventFormActions.LoadZones)
  loadZones(ctx: StateContext<EventFormStateModel>) {
    this.setEntityPending(ctx, zonesStateKey);
    return this.eventFormService.getZones()
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, zonesStateKey, parseServerTimeZones(result));
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, zonesStateKey, error);
        })
      );
  }

  @Action(EventFormActions.LoadJobPostings)
  loadJobPostings(ctx: StateContext<EventFormStateModel>) {
    this.setEntityPending(ctx, jobsStateKey);
    return this.eventFormService.getJobPostings()
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, jobsStateKey, result);
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, jobsStateKey, error);
        })
      );
  }

  @Action(EventFormActions.LoadCountries)
  loadCountries(ctx: StateContext<EventFormStateModel>) {
    this.setEntityPending(ctx, countriesStateKey);
    return this.eventFormService.getCounties()
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, countriesStateKey, {
            ...result,
            results: parseServerCountries(result.results)
          });
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, countriesStateKey, error);
        })
      );
  }

  private parseQueryParams(url: string) {
    if (!url) {
      return {};
    }
    const urlObj = new Url(url, true);
    return urlObj.query;
  }

  @Action(EventFormActions.LoadCities)
  loadCities(ctx: StateContext<EventFormStateModel>, {countryId, cityName}: EventFormActions.LoadCities) {
    if (!countryId) {
      return;
    }
    this.setEntityPending(ctx, citiesStateKey);
    return this.eventFormService.getCities(countryId, cityName)
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, citiesStateKey, {
            ...result,
            query: this.parseQueryParams(result.next),
            results: parseServerCities(result.results)
          });
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, citiesStateKey, error);
        })
      );
  }

  @Action(EventFormActions.ChangeCitiesSearch)
  changeCitiesSearch(ctx: StateContext<EventFormStateModel>, {searchStr}: EventFormActions.ChangeCitiesSearch) {
    const formState = EventFormState.formState(ctx.getState());
    const { country } = formState.model.location;
    if (country) {
      ctx.dispatch(new EventFormActions.LoadCities(country, searchStr));
    }
  }

  @Action(EventFormActions.GetNextCities)
  getNextCities(ctx: StateContext<EventFormStateModel>) {
    const citiesState = EventFormState.citiesState(ctx.getState());
    const { data } = citiesState;
    if (!data || !data.query.country_id) {
      return;
    }
    const { country_id, name, offset } = data.query;
    this.setEntityPending(ctx, citiesStateKey);
    return this.eventFormService.getCities(country_id, name, offset)
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, citiesStateKey, {
            ...result,
            query: this.parseQueryParams(result.next),
            results: [...data.results, ...parseServerCities(result.results)]
          });
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, citiesStateKey, error);
        })
      );
  }

  @Action(EventFormActions.UpdateCities)
  updateCities(ctx: StateContext<EventFormStateModel>, {countryId}: EventFormActions.UpdateCities) {
    if (countryId) {
      ctx.dispatch(new EventFormActions.LoadCities(countryId));
    }
    else {
      this.setEntityLoadSuccess(ctx, citiesStateKey, defaultEventFormState[citiesStateKey].data);
    }
  }

  @Action(EventFormActions.LoadZips)
  loadZips(ctx: StateContext<EventFormStateModel>, {cityId}: EventFormActions.LoadZips) {
    if (!cityId) {
      return;
    }
    this.setEntityPending(ctx, zipsStateKey);
    return this.eventFormService.getZips(cityId)
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, zipsStateKey, {
            ...result,
            results: parseServerZips(result.results)
          });
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, zipsStateKey, error);
        })
      );
  }

  @Action(EventFormActions.UpdateZips)
  updateZips(ctx: StateContext<EventFormStateModel>, {cityId}: EventFormActions.UpdateZips) {
    if (cityId) {
      ctx.dispatch(new EventFormActions.LoadZips(cityId));
    }
    else {
      this.setEntityLoadSuccess(ctx, zipsStateKey, defaultEventFormState[zipsStateKey].data);
    }
  }

  @Action(EventFormActions.LoadLetterTemplates)
  loadLetterTemplatesEventTypes(ctx: StateContext<EventFormStateModel>) {
    this.setEntityPending(ctx, letterTemplatesStateKey);
    return this.eventFormService.getLetterTemplates()
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, letterTemplatesStateKey, {
            ...result,
            results: parseServerLetterTemplates(result.results)
          });
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, letterTemplatesStateKey, error);
        })
      );
  }
}
