//!
//! \file
//!

//! \brief This is an example of running a simple schedule that includes an Application, a LPPM, an Attack, and a Metric

#include "include/Public.h" 

using namespace lpm;
int f(int user_start, int user_end, int tr_start, int tr_end, int loc_start, int loc_end,int lppm1,float lppm2, float lppm3, float ap, string actual_trace, string know,string output,int metric);

int convert_int(string ip);

float convert_float(string ip);

int convert_int(string ip){
  stringstream s(ip);
  int tmp;
  //s << ip;
  s >> tmp;
  //cout<<"converstion "<<tmp<<"\n";
  return tmp;
}

float convert_float(string ip){
  stringstream s(ip);
  float tmp;
  //s << ip;
  s >> tmp;
  //cout<<"converstion "<<tmp<<"\n";
  return tmp;
}

int main(int argc, char **argv){
    int user_start,user_end, tr_start, tr_end, loc_start, loc_end,lppm1,metric;
    string actual_trace, know,output;
    float lppm2, lppm3, ap; 
    fstream newfile;
    newfile.open("sample_sch.csv",ios::in);
    if(newfile.is_open()){
        string tp,tmp;
        while(getline(newfile,tp)){
            stringstream s(tp),str_cnv;
            vector<string> v;
            while (s >> tmp) v.push_back(tmp);
            if (v.size() == 16){
                if (v[0] != "percent_sample"){

                    user_start = convert_int(v[2]);
                    user_end  = convert_int(v[3]);
                    metric = convert_int(v[4]);
					output = v[5];
					tr_start = convert_int(v[6]);
					tr_end = convert_int(v[7]);         
					loc_start = convert_int(v[8]);
					loc_end = convert_int(v[9]);
					lppm1 = convert_int(v[10]);
					lppm2 = convert_float(v[11]);
					lppm3 = convert_float(v[12]);  
					ap = convert_float(v[13]);
					actual_trace = v[14]; 
					know = v[15];
                    f(user_start,user_end,tr_start,tr_end,loc_start,loc_end, lppm1, lppm2, lppm3, ap, actual_trace, know,output,metric);
                }
            }
        }
        newfile.close();
    }
}


int f(int user_start, int user_end, int tr_start, int tr_end, int loc_start, int loc_end, int lppm1, float lppm2, float lppm3, float ap, string actual_trace, string know,string output,int metric)
{
	LPM* lpm = LPM::GetInstance();	// get a pointer to the LPM engine (core class)

	Parameters::GetInstance()->AddUsersRange(user_start, user_end); // {2}
	

	Parameters::GetInstance()->SetTimestampsRange(tr_start, tr_end);  // consider only timestamps 7, 8, ..., 18, 19
	Parameters::GetInstance()->SetLocationstampsRange(loc_start, loc_end); // consider only locationstamps 1, 2, 3, 4, 5, 6, 7, 8

	Log::GetInstance()->SetEnabled(true); // [optional] enable the logging facilities
	Log::GetInstance()->SetOutputFileName(output); // [optional] set the log file name (here: output.log)

	// Tweak the template's parameters'
	SimpleScheduleTemplate::GetInstance()->SetApplicationParameters(Basic, ap);
	SimpleScheduleTemplate::GetInstance()->SetLPPMParameters(lppm1, GeneralStatisticsSelection, lppm2, lppm3);
	SimpleScheduleTemplate::GetInstance()->SetAttackParameter(Strong);
	if(metric == 1){
		SimpleScheduleTemplate::GetInstance()->SetMetricParameters(Anonymity);
	}else if(metric == 2){
		SimpleScheduleTemplate::GetInstance()->SetMetricParameters(Distortion);
	}else{
		SimpleScheduleTemplate::GetInstance()->SetMetricParameters(Entropy);
	}

	File knowledge(know);
	Schedule* schedule = SimpleScheduleTemplate::GetInstance()->BuildSchedule(&knowledge, "simple"); // build the schedule

	if(schedule == NULL) 
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl; // print the error message
		return -1;
	}

	std::cout << schedule->GetDetailString() << endl; // print a description of the schedule

	std::cout << "Running schedule...";

	File input(actual_trace);
	if(lpm->RunSchedule(schedule, &input, "output") == false) // run the schedule
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl; // print the error message
		return -1;
	}

	std::cout << " done!" << endl;

	schedule->Release(); // release the schedule object (since it is no longer needed)

	return 0;
}
