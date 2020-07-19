#include "include/Public.h"
#include <fstream>
#include <vector> 
#include<string>
#include <sstream> 
using namespace lpm;

bool run_schedule(int user_start,int user_end,int loc_start,int loc_end,int day_len,int day_cnt,int week_cnt,string input_trace, string output_file );
int convert_int(string ip);
int main(int argc, char **argv){
    int user_start,user_end, loc_start, loc_end, day_len, days, week_cnt;
    string input_trace , output_file; 
    fstream newfile;
    newfile.open("sample.csv",ios::in);
    if(newfile.is_open()){
        string tp,tmp;
        while(getline(newfile,tp)){
            stringstream s(tp),str_cnv;
            vector<string> v;
            while (s >> tmp) v.push_back(tmp);
            //cout<<"debug"<<" "<<tp <<"\n";
            if (v.size() == 9){
                if (v[0] != "user_start"){
                    //cout<<"func_init"<<"\n";
                    user_start = convert_int(v[0]);
                    user_end  = convert_int(v[1]);
                    loc_start = convert_int(v[2]); 
                    loc_end = convert_int(v[3]);
                    day_len = convert_int(v[4]);
                    days = convert_int(v[5]); 
                    week_cnt = convert_int(v[6]);
                    input_trace = v[7];
                    output_file = v[8];
                    //cout<<"run_start"<<"\n";            
                    run_schedule(user_start,user_end, loc_start, loc_end, day_len, days, week_cnt,input_trace , output_file);
		    //cout<<"run loop end" << "\n";
                }
            }
        }
        newfile.close();
    }
}
int convert_int(string ip){
  stringstream s(ip);
  int tmp;
  //s << ip;
  s >> tmp;
  //cout<<"converstion "<<tmp<<"\n";
  return tmp;
}
bool run_schedule(int user_start,int user_end,int loc_start,int loc_end,int day_len,int day_cnt,int week_cnt,string input_trace, string output_file )
{
	LPM* lpm = LPM::GetInstance();	// get a pointer to the LPM engine (core class)

	Parameters::GetInstance()->AddUsersRange(user_start,user_end);
	//Parameters::GetInstance()->RemoveUsersRange(3, 4); // consider only users 2 and 5 (i.e. {2, 3, 4, 5} \ {3, 4})

	ull timestamps = day_len * day_cnt; // 168
	Parameters::GetInstance()->SetTimestampsRange(1, timestamps); // consider only timestamps 1, 2, 3, ..., 168
	Parameters::GetInstance()->SetLocationstampsRange(loc_start, loc_end); // consider only locationstamps 1, 2, 3, 4, 5, 6, 7, 8

	Log::GetInstance()->SetEnabled(true); // [optional] enable the logging facilities
	Log::GetInstance()->SetOutputFileName("output"); // [optional] set the log file name (here: output.log)

	File learningTraceFile(input_trace, true); // the learning trace file (in the current directory), read-only mode
	File outputKC(output_file, false); // the name of the output (the knowledge), write mode

	KnowledgeInput knowledge;	// construct and fill in the knowledge input
	knowledge.transitionsFeasibilityFile = NULL;	// a NULL pointer as transitions feasibility file means users can go from any location to any location
	knowledge.transitionsCountFile = NULL;	// a NULL pointer as transitions count file means no transitions knowledge not encoded as learning trace
	knowledge.learningTraceFilesVector = vector<File*>();
	knowledge.learningTraceFilesVector.push_back(&learningTraceFile); // add a pointer to the learning trace file

	// simple time partitioning: one day partitioned into morning, afternoon, night
	ull dayLength = day_len; // time instants in a day
	ull days = timestamps / dayLength; // a week

	const ull weeks = week_cnt;
	TPNode* timePart = Parameters::GetInstance()->CreateTimePartitioning(1, weeks * days * dayLength); // partition a week

	TPNode* week = NULL;
	VERIFY(timePart->SliceOut(0, days * dayLength, weeks, &week) == true); // get the week

	TPNode* weekdays = NULL;
	VERIFY(week->SliceOut(0, dayLength, 1, &weekdays) == true); // get the week days (first 5 days)

	//TPNode* weekend = NULL;
	//VERIFY(week->SliceOut(5*dayLength, dayLength, 2, &weekend) == true); // get the weekend days

	// week days
	TimePeriod morningwd; morningwd.start = 7 * dayLength/24; morningwd.length=5 * dayLength/24; morningwd.id = 1; morningwd.dummy = false;
	TimePeriod afternoonwd; afternoonwd.start = 12 * dayLength/24; afternoonwd.length=7 * dayLength/24; afternoonwd.id = 2; afternoonwd.dummy = false;
	TimePeriod nightpart1; nightpart1.start = 0 * dayLength/24; nightpart1.length=7 * dayLength/24; nightpart1.id = 3; nightpart1.dummy = false;
	TimePeriod nightpart2; nightpart2.start = 19 * dayLength/24; nightpart2.length=5 * dayLength/24; nightpart2.id = 3; nightpart2.dummy = false;

	vector<TimePeriod> periods = vector<TimePeriod>();
	periods.push_back(morningwd);
	periods.push_back(afternoonwd);
	periods.push_back(nightpart1);
	periods.push_back(nightpart2);

	VERIFY(weekdays->Partition(periods) == true);

	// weekend (a single time period for each day)
	//TimePeriod we; we.start = 0 * dayLength/24; we.length=24 * dayLength/24; we.id = 4; we.dummy = false;

	periods.clear();
	//periods.push_back(we);

	//VERIFY(weekend->Partition(periods) == true);

	// print out the time partitioning
	string str = "";
	VERIFY(timePart->GetStringRepresentation(str) == true);
	std::cout << "Time Partitioning:" << endl << str << endl;

	Parameters::GetInstance()->SetTimePartitioning(timePart); // set the time partitioning


	std::cout << "Starting Knowledge Construction" << endl;

	ull maxGSIterations = 100; // do at most 100 iterations of Gibbs sampling per user
	ull maxSeconds = 30; // and spend at most 30 sec per user (whichever occurs first).
	if(lpm->RunKnowledgeConstruction(&knowledge, &outputKC, maxGSIterations, maxSeconds) == false)
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl;	// display the error that occur and exit gracefully.
		return -1;
	}

	std::cout << "Done!" << endl;

	return 0;	// all went well
}
