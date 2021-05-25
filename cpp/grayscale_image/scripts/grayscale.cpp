#include "grayscale.hpp"

int main( void ) {

    Mat image = imread("/home/heisendelta/Pictures/Avalon.png", IMREAD_COLOR);
    gcvimg::render_image_grayscale(image, true, true);

}
