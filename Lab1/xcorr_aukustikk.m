%% using crosscorelation to find the efficent delay between audio signals

fs=4000;

n = 0:15;
x = 0.84.^n;
y = circshift(x,5);
[c,lags] = xcorr(x,y);
stem(lags,c)

maxcorr=max(abs(c));

a=find(maxcorr==c);
b=lags(11);

time_delay=abs(b)/fs;