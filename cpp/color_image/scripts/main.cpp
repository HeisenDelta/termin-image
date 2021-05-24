// #include "main.hpp"
#include "optimized_image.hpp"
#include <chrono>

using namespace std;
using namespace std::chrono;


int run_code() {

    auto start = high_resolution_clock::now();

    Mat image = imread("/home/heisendelta/Pictures/Avalon.png", IMREAD_COLOR);
    // cvimg::render_image(image, true);
    cv_opt::render_image_opt(image, true, 0, 0.0);

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    return duration.count();

} 


int main( void ) {
    
    // int sum = 0;
    // for (int i = 0; i < 5; ++i) sum += run_code();

    // cout << (int) sum / 5 << "μs\n";
    Mat image = imread("/home/heisendelta/Pictures/Avalon.png", IMREAD_COLOR);
    cv_opt::render_image_opt(image, true, 0, 0.0);
    cout << "\n\n'";
    cv_opt::render_image_opt(image, true, 0, 0.15);

    uchar red = 0;
    uchar green = 130;
    uchar blue = 255;

    float hue, sat, light;
    // Sat and light are percentages from 0.0 to 1.0

    rgb_to_hsl(red, green, blue, hue, sat, light);
    cout << (float) red << ' ' << (float) green << ' ' << (float) blue << '\n';

    cout << hue << ' ' << sat << ' ' << light << '\n';
    float B = 0.01;
    if (light + B > 1.0) light = 1.0;
    else light += B;

    uchar new_red, new_green, new_blue;
    hsl_to_rgb(new_red, new_green, new_blue, hue, sat, light);
    cout << (float) new_red << ' ' << (float) new_green << ' ' << (float) new_blue << '\n';

}
