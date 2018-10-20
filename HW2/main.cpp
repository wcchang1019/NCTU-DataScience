#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <time.h>

using namespace std;
clock_t total = clock();

bool classifySubset(vector<int> test,vector<vector<int>> all)
{
	for(int i=0;i<test.size();i++){
        vector<int> new_arr = test;
        new_arr.erase(new_arr.begin()+i);
        int j=0;
        for(j=0;j<all.size();j++){
            if(all[j] == new_arr){
                break;
            }
        }
        if(j == all.size()){
            return false;
        }
	}
	return true;
}

vector<vector<int>> getCandidate(vector<vector<int>> L){
    vector<vector<int>> ans;
    for(int i = 0; i < int(L.size()); i++){
        for(int j = i + 1; j < int(L.size()); j++){
            vector<int> uni;
            set_union(L[i].begin(), L[i].end(), L[j].begin(), L[j].end(), back_inserter(uni));
            if(uni.size() == L[j].size()+1){
                int k = 0;
                for(k = 0; k < ans.size(); k++){
                   if(uni == ans[k]){
                        break;
                   }
                }
                if(k == ans.size()){
                    if(classifySubset(uni, L)){
                        ans.push_back(uni);
                    }
                }
            }
        }
    }
    return ans;
}

pair<vector<pair<vector<int>,int>>, vector<vector<int>>> countCandidate(vector<vector<int>> transactions, vector<vector<int>> candidate, int threshold){
    vector<pair<vector<int>,int>> votedPair;
    vector<vector<int>> nextCandidate;
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

int main(void)
{
    clock_t tStart = clock();
    float min_support = 0.1;
    //vector<pair<vector<int>,int>> selected_arr;
    freopen("sample2.in","r", stdin);
    vector<vector<int>> transactions;
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
    /*for(int i=0;i<1000;i++){
        if(count_arr[i] >= threshold){
                vector<int> vec;
                vec.push_back(i);
                selected_arr.push_back(make_pair(vec, count_arr[i]));
                Lone.push_back(vec);
        }
    }*/
    vector<vector<int>> Lone;
    fstream fp;
    fp.open("test.txt", ios::out | ios::trunc);
    for(int i=0;i<1000;i++){
        vector<int> vec;
        vec.push_back(i);
        Lone.push_back(vec);
    }
    for(;;){
        pair<vector<pair<vector<int>,int>>, vector<vector<int>>> test;
        clock_t tStart = clock();
        test = countCandidate(transactions, Lone, threshold);
        printf("countCandidate: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
        tStart = clock();
        for(auto x: test.first){
            /*for(auto y: x.first){
                cout << y ;
            }*/
            for(int yy=0;yy<x.first.size();yy++){
                fp << x.first[yy];
                if(yy!=x.first.size()-1){
                    fp << ",";
                }
            }
            fp << ":";
            fp << setprecision (4) << fixed << (float)x.second/(float)transactions.size() << endl;
        }
        printf("outputtime: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
        Lone.clear();
        tStart = clock();
        Lone = getCandidate(test.second);
        if(Lone.size() == 0){
            break;
        }
        printf("getCandidate: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
    }
    fp.close();
    printf("total: %.2fs\n", (double)(clock() - total)/CLOCKS_PER_SEC);

return 0;
}
