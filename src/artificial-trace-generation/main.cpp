//!
//! \file
//!

//! \brief This is an example of how to generate an artificial trace from a knowledge file

#include "include/Public.h" // the public header (Public.h) is the only header that should be included when linking with the library

using namespace lpm; // using the namespace allows to drop the lpm:: prefix in front of classes, structs etc...

int main(int argc, char **argv)
{
	LPM* lpm = LPM::GetInstance();	// get a pointer to the LPM engine (core class)

	Parameters::GetInstance()->AddUsersRange(1, 10); // consider simulated users ID 1, 2, 3, 4, 5
	Parameters::GetInstance()->SetTimestampsRange(1, 24); // consider timestamps 1, 2, 3, ..., 40
	Parameters::GetInstance()->SetLocationstampsRange(1, 81); // consider locationstamps 1, 2, 3, ..., 8

	Log::GetInstance()->SetEnabled(true); // [optional] enable the logging facilities
	Log::GetInstance()->SetOutputFileName("output"); // [optional] set the log file name (here: output.log)

	File knowledge("artificial.knowledge", true); // the knowledge file to use as input
	File output("artificial.trace", false); // the output file for the output of the generator (i.e. an actual artificial trace)

	std::cout << "Generating trace...";

	if(lpm->GenerateTracesFromKnowledge(&knowledge, &output) == false) // generate traces using the knowledge provided
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl;
		return -1;
	}

	std::cout << " done!" << endl;

	return 0;
}
