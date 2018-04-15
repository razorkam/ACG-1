#version 330 core
in vec3 vFragPosition;
in vec3 vNormal;

out vec4 color;


//just 256x2 pseudorandom integers in [0;255] range
int[512] p = int[](
    151,160,137,91,90,15,
    131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
    190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
    88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
    77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
    102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
    135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
    5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
    223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
    129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
    251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
    49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180,
    151,160,137,91,90,15,
    131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
    190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
    88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
    77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
    102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
    135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
    5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
    223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
    129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
    251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
    49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180);



vec2 fade(vec2 t)
{
    return pow(t,vec2(5))*6 - pow(t,vec2(4))*15 + pow(t,vec2(3))*10;
}

float linterp( float a, float b, float x ) // simple 1d linear interpolation
{
    return a + x * (b - a);
}


float dot_pr( int hash, float x, float y ) //get dot product of (x,y) dist vector and pseudorandom grad vector
{
    //pick one of 8 grad vectors
    switch( hash & 0x7 ) //last 3 bits
    {
       case 0x0: return y; // (0,1)
       case 0x1: return x+y; // (1,1)
       case 0x2: return x; // (1,0)
       case 0x3: return x-y; // (1,-1)
       case 0x4: return -y; // (0,-1)
       case 0x5: return -x-y; // (-1,-1)
       case 0x6: return -x; // (-1,-0)
       case 0x7: return -x+y; // (-1,-1)
       default: return 0.0;
    }
}



float perlin_noise_improved_2d( vec2 coords )
{
    ivec2 floored = ivec2(floor(coords));
    coords -= vec2(floored); //scale coords in [0;1] local coordinates


    // surrounding unit square
    // lu -- ru
    // -     -
    // -     -
    // ld -- rd

    // hash square angles coords
    floored &= 0xff; // use last byte: [0;255] to hash floored coords

    // hash andle coords to [0;255]
    int ld_hash = p[p[floored.x] + floored.y]; // 0 to 255
    int lu_hash = p[p[floored.x] + floored.y + 1];
    int rd_hash = p[p[floored.x + 1] + floored.y];
    int ru_hash = p[p[floored.x + 1] + floored.y + 1];

    //get dot pr. of picked grad and dist vector
    float ld_val = dot_pr(ld_hash, coords.x, coords.y);
    float lu_val = dot_pr(lu_hash, coords.x, coords.y-1);
    float ru_val = dot_pr(ru_hash, coords.x-1, coords.y-1);
    float rd_val = dot_pr(rd_hash, coords.x-1, coords.y);

    coords = fade(coords); //smoothly fade coordinates

    //bilinear interpolating
    float x1 = linterp(lu_val, ru_val, coords.x);
    float x2 = linterp(ld_val, rd_val, coords.x);
    float linterped_val = linterp(x1,x2,coords.y);

    return (linterped_val + 2) / 4.0; // [0;1] scale???
}


float octave_perlin_noise(vec2 xy, int octaves, float persistance )
{
  float res = 0;
  float frequency = 1.0;
  float amplitude = 10.0;
  float max = 0;


  for(int i=0; i<octaves; ++i )
  {
     res += perlin_noise_improved_2d(xy*frequency) * amplitude;
     max += amplitude;
     amplitude *= persistance;
     frequency *= 2;
  }

  return clamp(res/max, 0.0, 1.0);
}

void main()
{
    float noise = octave_perlin_noise(vFragPosition.xz, 6, 0.3);

//    vFragPosition.y = noise;
    color = vec4(vec3(noise), 1.0);
}