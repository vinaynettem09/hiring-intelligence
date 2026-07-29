// Mirrors app/modules/consent/schemas.py.

export interface ConsentSection {
  key: string;
  title: string;
  body: string;
}

export interface ConsentDisclosure {
  version: string;
  sections: ConsentSection[];
}

export interface ConsentState {
  organization_name: string;
  role_title: string;
  candidate_name: string;
  disclosure: ConsentDisclosure;
  consented: boolean;
  next_step: "work_sample";
}
