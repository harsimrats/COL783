#include <iostream>
#include <fstream>


#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;
int source[50][2], deste[50][2];int st,dt; int i,j; int globnii,globnoi;int p,l;char id[2]; int w,h; int max_pixel;

char si = 'S';
char di = 'D';

float intm[20][200][3][2]; int i,j,k,l; float alpha, beta;
float gama;
int sred[512][512],sgreen[512][512],sblue[512][512], dred[512][512],dgreen[512][512], dblue[512][512];
char id2[2]; int w2,h2; int max_pixel2;
int intm_pixelred[20][512][512];int intm_pixelgreen[20][512][512];int intm_pixelblue[20][512][512];

class Color
{
	private:
		int red;
		int green;
		int blue;

	public:
		Color()
		{
			setColor(0, 0, 0);
		}

		void setColor(int r, int g, int b)
		{
			setRed(r);
			setGreen(g);
			setBlue(b);
		}

		void setRed(int r)
		{
			red = r;
		}

		void setGreen(int g)
		{
			green = g;
		}

		void setBlue(int b)
		{
			blue = b;
		}

		int getRed() const
		{
			return red;
		}

		int getGreen() const
		{
			return green;
		}

		int getBlue() const
		{
			return blue;
		}
}src[512][512],dst[512][512];

class Image
{
	private:
		char type[5];
		int width, height;
		int max_val;
		Color **color;

		Mat convertToCvImage()
		{
			Mat img(height, width, CV_8UC3);

			for(int i = 0; i < height; i++)
			{
				for(int j = 0; j < width; j++)
				{
					img.at<Vec3b>(i, j) = Vec3b(color[i][j].getBlue(), color[i][j].getGreen(), color[i][j].getRed());
				}
			}

			return img;
		}

	public:
		Image()
		{
			strcpy(type, "\0");
			width = 0;
			height = 0;
			max_val = 0;
			color = NULL;
		}

		bool readImage(char filename[])
		{
			ifstream file;
			file.open(filename, ios::in);

			if(file.good())
			{
				file >> type;
				file >> width >> height;
				file >> max_val;

				color = new Color*[height];
				for(int i = 0; i < height; i++)
				{
					color[i] = new Color[width];

					for(int j = 0; j < width; j++)
					{
						int r, g, b;
						file >> r >> g >> b;
						color[i][j].setColor(r, g, b);
					}
				}

				file.close();

				return true;
			}
			else
			{
				cerr << "Error reading image: " << filename << endl;
				return false;
			}
		}

		bool writeImage(char filename[])
		{
			ofstream file;
			file.open(filename, ios::out);

			if(file.good())
			{
				file << type << endl;
				file << width << " " << height << endl;
				file << max_val << endl;

				for(int i = 0; i < height; i++)
				{
					for(int j = 0; j < width; j++)
					{
						file << color[i][j].getRed() << " " << color[i][j].getGreen() << " " << color[i][j].getBlue() << endl;
					}
				}

				file.close();
				return true;
			}
			else
			{
				cerr << "Error writing file: " << filename << endl;
				return false;
			}
		}

		static bool writeVideo(Image images[], int num_images, char filename[])
		{
			if(num_images == 0)
			{
				cerr << "No frames to write" << endl;
				return false;
			}

			VideoWriter outputVideo;
			Size frame_size = Size(images[0].width, images[0].height);

			outputVideo.open(filename, 861292868, 25, frame_size, true);	// 3rd argument is the frame rate

			if (!outputVideo.isOpened())
			{
				cerr << "Unable to write video: " << filename << endl;
				return false;
			}

			for(unsigned int f = 0; f < num_images; f++)
			{
				outputVideo << images[f].convertToCvImage();
			}

			return true;
		}
};

// TODO: Add your classes here

class triangle
{	int b[50][2];
	int a[50][2];
	int pos=3;
	int inp_numb[50];
	int sort_numb[50];
	int edge[50][500];
	int shiedge[500];
	int tria[100][3];

	public:
		int retptorigx(int);
		int retptorigy(int);
		int retptx(int);
		int retpty(int);
		void coord_assign(int t[][2]);
		void coord_assign_orig(int t[][2]);
		void sort();
		int poi(int, int, int, int, int, int, int, int);
		void edge_comp(int);
		void tb();
		void trisortint();
		void trisortext();
		int rettri(int, int);
		void inp_assign();
		void sort_assign();
		void shiedge_assign();
		int retinpnumb(int);
		int retsortnumb(int);
		int retedge(int,int);
		int retshiedge(int);
		int retpos();
};
triangle s;

//pos is 1 greater than the lements in final edge ie edge[14]

int triangle::retedge(int i,int j)
{
	return edge[i][j];
}

int triangle::retpos()
{
	return pos;
}

int triangle::retshiedge(int i)
{
	return shiedge[i];
}

int triangle::retinpnumb(int i)
{
	return inp_numb[i];
}

int triangle::retsortnumb(int i)
{
	return sort_numb[i];
}

int triangle::retptorigx(int i)
{
	return b[i][0];
}

int triangle::retptorigy(int i)
{
	return b[i][1];
}
int triangle::retptx(int i)
{
	return a[i][0];
}

int triangle::retpty(int i)
{
	return a[i][1];
}

void triangle::coord_assign(int t[50][2])
{
	for(i=0;i<globnii;i++)
	{
		a[i][0]=t[i][0];
		a[i][1]=t[i][1];
	}
}
void triangle::coord_assign_orig(int t[50][2])
{
	for(i=0;i<globnii;i++)
	{
		b[i][0]=t[i][0];
		b[i][1]=t[i][1];
	}
}
void triangle::shiedge_assign()
{
	for(i=0;i<pos-1;i++)
{
	shiedge[i]=inp_numb[(edge[globnii-1][i]-1)];
}
}

void triangle::inp_assign()
{
	for(i=0;i<globnii;i++)
		inp_numb[i]=i+1;
}

void triangle::sort_assign()
{
	for(i=0;i<globnii;i++)
		{	sort_numb[i]=i+1;}
}

void triangle::sort()
{	int min;int loc,locy; int temp;int sy;
	for(p=0;p<=globnii-1;p++)
	{
	min=a[p][0];
	sy=a[p][1];
	loc=p;

	for(j=p+1;j<=globnii-1;j++)
	{
		if(min>a[j][0])
		{
			min=a[j][0];
			loc=j;
		}
		else if(min==a[j][0])
		{
			if(sy>a[j][1])
			{
				sy=a[j][1];
				locy=j;
				temp=a[p][0];
				a[p][0]=a[locy][0];
				a[locy][0]=temp;
				temp=a[p][1];
				a[p][1]=a[locy][1];
				a[locy][1]=temp;

				temp=inp_numb[p];
				inp_numb[p]=inp_numb[locy];
				inp_numb[locy]=temp;
			}
		}
	}

	temp=a[p][0];
	a[p][0]=a[loc][0];
	a[loc][0]=temp;
	temp=a[p][1];
	a[p][1]=a[loc][1];
	a[loc][1]=temp;

	temp=inp_numb[p];
	inp_numb[p]=inp_numb[loc];
	inp_numb[loc]=temp;

	}
}
int triangle::poi(int p1x,int p2x,int p3x,int p4x,int p1y,int p2y,int p3y,int p4y)
{float a1,a2,b1,b2,c1,c2;float x,y, slope;


a1=p2y-p1y;
b1=-(p2x-p1x);
c1=(p2x*p1y)-(p1x*p2y);
//cout<<a1<<"  as  "<<b1<<"  asdasdasd  "<<c1<<endl;
a2=p4y-p3y;
b2=-(p4x-p3x);
c2=(p4x*p3y)-(p3x*p4y);
//cout<<a2<<"  bs  "<<b2<<"  bsdasdasd  "<<c2<<endl;
if((a1*p3x+b1*p3y+c1)*(a1*p4x+b1*p4y+c1)<0)
{
x = (b1*c2 - b2*c1)*1.0/(a1*b2 - a2*b1)*1.0;
y = (c1*a2 - c2*a1)*1.0/(a1*b2 - a2*b1)*1.0;
slope=(x-p1x)/(p2x-p1x);

if(slope>0 && slope<1)
	return 1;
else
	return 0;

}
else if((a1*p3x+b1*p3y+c1)==0 && (a1*p4x+b1*p4y+c1)==0)
	{return 1;}
else if(((a1*p3x+b1*p3y+c1)==0 && (a1*p4x+b1*p4y+c1)!=0) || ((a1*p3x+b1*p3y+c1)!=0 && (a1*p4x+b1*p4y+c1)==0))
{return 0;}
else
	return 0;
}

void triangle::edge_comp(int n)
{
	if(n==2)
	{
		edge[1][0]=1; edge[1][1]=2; pos=3;	edge[1][2]=-20;
		cout<<"\nyeh func wala h:"<<edge[1][2];

	}
	else
	{
		int tx,ty; int r[500],temp,k=0; int flag=0;
		for(i=0;i<pos;i++)
			edge[n-1][i]=edge[n-2][i];

		for(j=0;edge[n-1][j]!=-20;j+=2) //some error in that != condition.
			{	flag=0;
			for(p=0;p<(pos-1);p+=2)
			{
				tx=edge[n-1][p];
				ty=edge[n-1][p+1];
				r[p]=poi(a[tx-1][0],a[ty-1][0],a[k][0],a[n-1][0],a[tx-1][1],a[ty-1][1],a[k][1],a[n-1][1]);
				if(r[p]==1)
					{flag=1;break;}
			}
			if (flag==0)
				{
					temp=pos-1; pos=pos+2;

						edge[n-1][temp]=k+1;
						edge[n-1][temp+1]=n;
						edge[n-1][temp+2]=-20;
				}
			k++;
			cout<<"\nyeh func wala h:"<<edge[1][2];

			if(n-k==1)
				j=pos-3;
			}


	}
	return;

}

int triangle::rettri(int i, int j)
{
	return tria[i][j];
}

void triangle::tb()
{
	int t1,t2,t3,t4,t5,t6;l=0;int flaggy=0;j=2;int k;int d_flag=1;int s_flag=1;
	for(i=0;i<=pos-3;i+=2)
	{	flaggy=0;d_flag=1;s_flag=1;
		t1=shiedge[i];
		t2=shiedge[i+1];

		for(j=i+2;j<=pos-3;j+=2)
		{	j=i+2;
			t3=shiedge[j];
			t4=shiedge[j+1];
		do
		{
		k=j+2;
			if(t1==t3)
			{
				t5=shiedge[k];
				t6=shiedge[k+1];
					do
					{

						if(t2==t5 && t4==t6)
						{
							tria[l][0]=t1;
							tria[l][1]=t2;
							tria[l][2]=t4;
							l++;flaggy=1;break;
						}
						else
						{
							k+=2;
						t5=shiedge[k];
						t6=shiedge[k+1];
							d_flag=0;
						}
					}while(d_flag==0 && k<=pos-3);
					if(flaggy==1)
					break;
			}
			else
			{
				j+=2;k=j+2;
					t3=shiedge[j];
					t4=shiedge[j+1];
					s_flag=0;

			}



		}while(s_flag==0 && j<=pos-3);
		if(flaggy==1)
		break;
		}
	}
}

void triangle::trisortint()
{
	int k,temp;
for(k=0;k<l;k++)
{
	for(i=1;i<3;++i)
    {
        for(j=0;j<(3-i);++j)
            if(tria[k][j]>tria[k][j+1])
            {
                temp=tria[k][j];
                tria[k][j]=tria[k][j+1];
                tria[k][j+1]=temp;
            }
    }
}
}

void triangle::trisortext()
{int temp;
for(i=1;i<l;++i)
    {
        for(j=0;j<(l-i);++j)
            if(tria[j][0]>tria[j+1][0])
            {
                temp=tria[j][0];
                tria[j][0]=tria[j+1][0];
                tria[j+1][0]=temp;

                temp=tria[j][1];
                tria[j][1]=tria[j+1][1];
                tria[j+1][1]=temp;

				temp=tria[j][2];
                tria[j][2]=tria[j+1][2];
                tria[j+1][2]=temp;
            }
            else if(tria[j][0]==tria[j+1][0])
            {
            	if(tria[j][1]>tria[j+1][1])
            	{
                temp=tria[j][0];
                tria[j][0]=tria[j+1][0];
                tria[j+1][0]=temp;

                temp=tria[j][1];
                tria[j][1]=tria[j+1][1];
                tria[j+1][1]=temp;

				temp=tria[j][2];
                tria[j][2]=tria[j+1][2];
                tria[j+1][2]=temp;
            	}
            	else if(tria[j][1]==tria[j+1][1])
            	{
            		if(tria[j][2]>tria[j+1][2])
            		{
                temp=tria[j][0];
                tria[j][0]=tria[j+1][0];
                tria[j+1][0]=temp;

                temp=tria[j][1];
                tria[j][1]=tria[j+1][1];
                tria[j+1][1]=temp;

				temp=tria[j][2];
                tria[j][2]=tria[j+1][2];
                tria[j+1][2]=temp;
            		}
				}
			}
    }
}

Mat source_image;
Mat destination_image;

void on_mouse(int event, int x, int y, int flags, void *param)
{
	if(event == EVENT_LBUTTONDOWN)
	{
		char im_type = *(char *) param;

		if(im_type == si) 						// Clicked on source image
		{
			for(int i = y - 2; i <= y + 2; i++)
			{
				for(int j = x - 2; j <= x + 2; j++)
				{
					source_image.at<Vec3b>(i, j) = Vec3b(255, 0, 0);
				}
			}
			source[st][0]=x;	source[st][1]=y;
						st++;
			imshow("Source Image", source_image);
			waitKey(0);
		}
		else if(im_type == di)					// Clicked on destination image
		{
			for(int i = y - 2; i <= y + 2; i++)
			{
				for(int j = x - 2; j <= x + 2; j++)
				{
					destination_image.at<Vec3b>(i, j) = Vec3b(255, 0, 0);
				}
			}
			deste[dt][0]=x;	deste[dt][1]=y;
						dt++;
			imshow("Destination Image", destination_image);
			waitKey(0);
		}

		// TODO: Write your code for mouse click here
	}
}

int main()
{
	char src[50];
	char dest[50];
	int NumOutputImages;
	int NumClicks;

	cin >> src >> dest;
	cin >> NumOutputImages >> NumClicks;
	globnii=NumClicks+4;
	globnoi=NumOutputImages;

	source_image = imread(src);
	destination_image = imread(dest);

	namedWindow("Source Image");
	namedWindow("Destination Image");

	setMouseCallback("Source Image", on_mouse, &si);
	setMouseCallback("Destination Image", on_mouse, &di);

	imshow("Source Image", source_image);
	imshow("Destination Image", destination_image);

	waitKey(0);


	// TODO: Write your code for morphing here

	/*int fr=st+4;
	for(;st<fr;st++)
	{
		source[st]
	}*/

	ifstream f;

	   	f.open(src,ios::in);

	    	if(!f.good())
	    		cerr<<"IMAGE NOT FOUND"<<endl;
	        f >> id;f>>w;f>>h;f>>max_pixel;
	        f.close();
	        source[st][0]=0;
	        source[st][1]=0;
	        st++;
	        source[st][0]=w-1;
	        source[st][1]=0;
	        st++;
	        source[st][0]=0;
	        source[st][1]=h-1;
	        st++;
	        source[st][0]=w-1;
	        source[st][1]=h-1;
	        st++;

	        deste[st][0]=0;
	        	        deste[st][1]=0;
	        	        dt++;
	        	        deste[st][0]=w-1;
	        	        deste[st][1]=0;
	        	        dt++;
	        	        deste[st][0]=0;
	        	        deste[st][1]=h-1;
	        	        dt++;
	        	        deste[st][0]=w-1;
	        	        deste[st][1]=h-1;
	        	        dt++;


		for(i=0;i<st;i++)
				{for(j=0;j<2;j++)
					cout<<source[i][j]<<" ";
					cout<<endl;
				}
	//cout<<globnii<<globnoi<<endl;
	s.coord_assign(source);
	s.coord_assign_orig(source);

	//for checking a and b matrix;
	/*for(i=0;i<globnii;i++)
					{
						cout<<s.retptx(i)<<" "<<s.retpty(i);
						cout<<endl;
					}
	for(i=0;i<globnii;i++)
						{
							cout<<s.retptorigx(i)<<" "<<s.retptorigy(i);
							cout<<endl;
						}*/


	//cout<<st<<" "<<dt<<" ";cout<<destinp[4];
			s.inp_assign();
		/*for(i=0;i<globnii;i++)
		{
			cout<<s.retinpnumb(i);
		}*/
			//working fine till now
			s.sort();
			/*for(i=0;i<globnii;i++)
								{
									cout<<s.retptx(i)<<" "<<s.retpty(i);
									cout<<endl;
								}
				sort also working fine*/

			s.sort_assign();
			/*for(i=0;i<globnii;i++)
					{
						cout<<s.retsortnumb(i);
					}
			cout<<endl;
			for(i=0;i<globnii;i++)
					{
						cout<<s.retinpnumb(i);
					}working fine till now*/
			cout<<endl;//cout<<"global"<<globnii;


			/*for(i=2;i<=globnii;i++)
			{
				s.edge_comp(i);
				cout<<"\npos="<<s.retpos();
				for(j=0;j<s.retpos();j++)
					cout<<"\n"<<s.retedge(i-1,j)<<" ";
				cout<<endl;

			}*/
			/*s.edge_comp(2);
			cout<<"\npos="<<s.retpos();
			for(j=0;j<s.retpos();j++)
			cout<<"\n"<<s.retedge(1,j)<<" ";
			cout<<endl;
			s.edge_comp(3);*/
			s.edge_comp(2);
			/*cout<<"\npos="<<s.retpos();
			for(j=0;j<s.retpos();j++)
			cout<<"\n"<<s.retedge(1,j)<<" ";
			cout<<endl;*/
			s.edge_comp(3);
				/*cout<<"\npos="<<s.retpos();
				for(j=0;j<s.retpos();j++)
				cout<<"\n"<<s.retedge(2,j)<<" ";
				cout<<endl;*/
			s.edge_comp(4);
				/*cout<<"\npos="<<s.retpos();
				for(j=0;j<s.retpos();j++)
				cout<<"\n"<<s.retedge(3,j)<<" ";
				cout<<endl;*/
			s.edge_comp(5);
						/*cout<<"\npos="<<s.retpos();
			for(j=0;j<s.retpos();j++)
				cout<<"\n"<<s.retedge(4,j)<<" ";
			cout<<endl;
				*/
			s.edge_comp(6);
/*cout<<"\npos="<<s.retpos();
or(j=0;j<s.retpos();j++)
	cout<<"\n"<<s.retedge(5,j)<<" ";
	cout<<endl;*/

		s.edge_comp(7);
			/*cout<<"\npos="<<s.retpos();
				for(j=0;j<s.retpos();j++)
cout<<"\n"<<s.retedge(6,j)<<" ";
		cout<<endl;
*/

	 		s.shiedge_assign();
			s.tb();

			s.trisortint();
			s.trisortext();
			/*for(i=0;i<l;i++)
			{	cout<<"TRIANGLE:\n\n";
				for(j=0;j<3;j++)
					cout<<s.rettri(i,j)<<" ";
				cout<<endl;
			}*/



	return 0;
}
