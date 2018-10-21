#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <time.h>
#include <omp.h>
#include <math.h>
#include <sstream>

using namespace std;
clock_t total = clock();

bool classifySubset(vector<int> test,vector<vector<int> > all)
{
	for(int i=0;i<test.size();i++){
        vector<int> new_arr = test;
        new_arr.erase(new_arr.begin()+i);
        if(find(all.begin(), all.end(), new_arr) == all.end()){
            return false;
        }
	}
	return true;
}

vector<vector<int> > getCandidate(vector<vector<int> > L){
    vector<vector<int> > ans;
    vector< vector<int> >::iterator row, rowadd;
    int len = L[0].size();
    for(row = L.begin(); row != L.end(); ++row){
        for(rowadd = row + 1; rowadd < L.end(); rowadd++){
            vector<int> uni;
            set_union(row->begin(), row->end(), rowadd->begin(), rowadd->end(), back_inserter(uni));
            if(uni.size() == len+1){
                if(find(ans.begin(), ans.end(), uni) != ans.end()){
                    break;
                }else{
                    if(classifySubset(uni, L)){
                        ans.push_back(uni);
                    }
                }
            }
        }
    }
    return ans;
}

pair<vector<pair<vector<int>,int> >, vector<vector<int> > > countCandidate(vector<vector<int> > transactions, vector<vector<int> > candidate, int threshold){
    vector<pair<vector<int>,int> > votedPair;
    vector<vector<int> > nextCandidate;
    for(int i = 0;i < candidate.size(); i++){
        int cnt = 0;
        for(int j = 0;j < transactions.size(); j++){
            vector<int> intersect;
            set_intersection(transactions[j].begin(), transactions[j].end(),
                      candidate[i].begin(), candidate[i].end(), back_inserter(intersect));
            if(intersect == candidate[i]){
                cnt++;
            }
        }
        if(cnt >= threshold){
            votedPair.push_back(make_pair(candidate[i],cnt));
            nextCandidate.push_back(candidate[i]);
        }
    }
    return make_pair(votedPair,nextCandidate);
}

int main(int argc, char *argv[])
{
    clock_t tStart = clock();
    istringstream aaaa(argv[1]);
    float min_support;
    aaaa >> min_support;
    FILE *fPtr;
    fPtr = freopen(argv[2], "r", stdin);
    if (!fPtr) {
        printf("open file failed");
        exit(1);
    }
    vector<vector<int> > transactions;
    string line;
    while(!getline(cin, line).eof()){
        vector<int> arr;
        istringstream ssline(line);
        string number;
        while(getline(ssline, number, ',')){
            arr.push_back(atoi(number.c_str()));
        }
        transactions.push_back(arr);
    }
    int threshold = min_support*int(transactions.size());
    vector<vector<int> > Lone;
    fstream fp;
    fp.open(argv[3], ios::out | ios::trunc);
    for(int i=0;i<1000;i++){
        vector<int> vec;
        vec.push_back(i);
        Lone.push_back(vec);
    }
    for(;;){
        pair<vector<pair<vector<int>,int> >, vector<vector<int> > > test;
        clock_t tStart = clock();
        test = countCandidate(transactions, Lone, threshold);
        //printf("countCandidate: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
        tStart = clock();
        vector<pair<vector<int>,int> >::iterator x;
        for(x=test.first.begin();x<test.first.end();++x){
        //for(auto x: test.first){
            for(int yy=0;yy<x->first.size();yy++){
                fp << x->first[yy];
                if(yy!=x->first.size()-1){
                    fp << ",";
                }
            }
            float ans = floor(((float)x->second*10000/(float)transactions.size()) + 0.5) / 10000.;
            fp << ":";
            fp << setprecision (4) << fixed << ans << endl;
        }
        //printf("outputtime: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
        Lone.clear();
        tStart = clock();
        Lone = getCandidate(test.second);
        if(Lone.size() == 0){
            break;
        }
        //printf("getCandidate: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
    }
    fp.close();
    //printf("total: %.2fs\n", (double)(clock() - total)/CLOCKS_PER_SEC);

return 0;
}
