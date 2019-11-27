#include <memory>
#include <vector>
class State;
typedef std::vector<std::unique_ptr<State>> StateCollection;

class State {
	std::unique_ptr<StateCollection> mine;
	void unroll();
	
	void step(int depth) {
		if(mine != nullptr) for(auto & st : *mine) st->step(depth);
		else stepNew(depth);
	}
	
	void stepNew(int depth) {
		if(depth == 0) return;
		unroll();
		for(auto & st : *mine) st->step(depth - 1);
	}
	
	std::pair<int, int> route(char type) {
		int quantity = mine->size();
		int values[quantity];
		int score;
		int j;
		for(int i = 0; i != quantity; i++) {
			values[i] = mine->at(i)->route(-type).first;
		}
		if(type == 1) {
			score = values[0];
			for(int i = 1; i != quantity; i++) {
				if(values[i] > score) {
					score = values[i];
					j = i;
				}
			}
		}
		else if(type == -1) {
			score = values[0];
			for(int i = 1; i != quantity; i++) {
				if(values[i] < score) {
					score = values[i];
					j = i;
				}
			}
		}
		return std::pair<int, int>(score, j);
	}
	
	std::unique_ptr<State> Descend(const State & compare) {
		//ten argument
		//to nie jest state tylko jakaś inna klasa
		for(auto & st : *mine) if(*st == compare) return std::move(st);
	} 
	//on ma policzone wszystkie dzieci
	// a potem na nim trzeba wywołać step(1)
};



