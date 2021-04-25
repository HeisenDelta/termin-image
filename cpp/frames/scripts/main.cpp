#include "main.hpp"

int main( void ) {

    Mat image = imread("/home/heisendelta/Pictures/Avalon.png", IMREAD_COLOR);
    cvimg::render_image(image, true);

}
