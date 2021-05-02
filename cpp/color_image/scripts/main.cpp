// #include "main.hpp"
#include "optimized_image.hpp"
#include <chrono>

using namespace std;
using namespace std::chrono;


int run_code() {

    auto start = high_resolution_clock::now();

    Mat image = imread("/home/heisendelta/Pictures/Avalon.png", IMREAD_COLOR);
    // cvimg::render_image(image, true);
    cv_opt::render_image_opt(image, true, 0);

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    return duration.count();

} 


int main( void ) {
    
    int sum = 0;
    for (int i = 0; i < 5; ++i) sum += run_code();

    cout << (int) sum / 5 << "μs\n";

}
