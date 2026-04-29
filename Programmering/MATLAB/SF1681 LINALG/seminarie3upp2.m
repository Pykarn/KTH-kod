

img = imread("Bild.jpg");
gray = rgb2gray(img);
A = double(gray);

figure
imshow(A,[0 255])

s = svd(A);
x_plot=1:length(s);

figure
plot(x_plot, s, LineWidth=2)
xlabel('Index');
ylabel('Singularvärde');


[Y,S,X] = svd(A);

X=X';


B=zeros(720, 1280);
%rank(S)
for i=1:92
    B=B+s(i)*Y(:,i)*X(i,:);
end




figure
imshow(B,[0 255])

