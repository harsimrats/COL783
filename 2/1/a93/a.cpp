#include<fstream>
#include<iostream>
#include<math.h>
#include<stdio.h>
#include<string.h>

using namespace std;

int i,j;int p;int l;int cro[50][2];

class triangle
{
	int a[50][2];
	int pos=3;
	int inp_numb[50];
	int sort_numb[50];
	int edge[50][500];
	int shiedge[500];
	int tria[100][3];

	public:

		void coord_assign(int a[][2]);
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
		void show();
};
triangle t;

//pos is 1 greater than the lements in final edge ie edge[14]

void triangle::show()
{
	for(i=0;i<100;i+=2)
	{
		cout<<edge[13][i]<<" "<<edge[13][i+1]<<endl;
	}
}
void read()
{   ifstream f;

	f.open("input1.txt",ios::in);

	if(!f.good())
		cerr<<"FILE NOT FOUND"<<endl;

	for(i=0;i<14;i++)
	{	for(j=0;j<2;j++)
		f>>cro[i][j];

	}
		f.close();
}

void triangle::coord_assign(int cro[50][2])
{
	for(i=0;i<50;i++)
	{
		a[i][0]=cro[i][0];
		a[i][1]=cro[i][1];
	}
}

void triangle::shiedge_assign()
{
	for(i=0;i<pos-1;i++)
{
	shiedge[i]=inp_numb[(edge[13][i]-1)];
}
}

void triangle::inp_assign()
{
	for(i=0;i<14;i++)
		inp_numb[i]=i+1;
}

void triangle::sort_assign()
{
	for(i=0;i<14;i++)
		{	sort_numb[i]=i+1;}
}

void triangle::sort()
{	int min;int loc,locy; int temp;int sy;
	for(p=0;p<=13;p++)
	{
	min=a[p][0];
	sy=a[p][1];
	loc=p;

	for(j=p+1;j<=13;j++)
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

void write()
{
	ofstream fout;

	fout.open("output.txt",ios::out);

	if(!fout.good())
		cerr<<"FILE NOT FOUND"<<endl;

	for(i=0;i<l;i++)
	{	for(j=0;j<3;j++)
		fout<<t.rettri(i,j)<<" ";
		fout<<endl;

	}
		fout.close();

}

int main()
{	//triangle t;


	read();
	t.coord_assign(cro);
	t.inp_assign();
	t.sort();
	t.sort_assign();
	t.edge_comp(2);
	t.edge_comp(3);
	t.edge_comp(4);
	t.edge_comp(5);
	t.edge_comp(6);
	t.edge_comp(7);
	t.edge_comp(8);
	t.edge_comp(9);
	t.edge_comp(10);
	t.edge_comp(11);
	t.edge_comp(12);
	t.edge_comp(13);
	t.edge_comp(14);
/*for(i=0;i<pos;i+=2)
{
	cout<<edge[13][i]<<" "<<edge[13][i+1]<<endl;
}
cout<<endl<<endl<<endl;*/
t.show();
t.shiedge_assign();
/*for(i=0;i<pos-1;i+=2)
{
	cout<<shiedge[i]<<" "<<shiedge[i+1]<<endl;
}*/
t.tb();
t.trisortint();
t.trisortext();
/*for(i=0;i<l;i++)
{
	cout<<tria[i][0]<<" "<<tria[i][1]<<" "<<tria[i][2]<<endl;
}*/
write();
return 0;
}





