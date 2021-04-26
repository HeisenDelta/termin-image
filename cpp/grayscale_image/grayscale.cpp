#include "grayscale.hpp"

int main( void ) {

    Mat image = imread("/home/heisendelta/Pictures/Avalon.png", IMREAD_GRAYSCALE);
    gcvimg::render_image_grayscale(image, true);

}
