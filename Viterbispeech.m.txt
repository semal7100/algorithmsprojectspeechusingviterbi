
function [Fopt, varargout]=viterbi_hmm(V, mean_vec_i, var_vec_i, a_i_j)
flag_plot_path=0;
if nargin==0
    V=[20 30 40 10 0 30]; 
    mean_vec_i=[NaN 10 40 -10 20 NaN];
    var_vec_i= [NaN  1  1   1  1 NaN];
    a_i_j=[0  0.8 0.2  0   0   0
        0  0.6 0.3 0.1  0   0
        0   0  0.6 0.3 0.1  0
        0   0   0  0.6 0.3 0.1
        0   0   0   0  0.6 0.4
        0   0   0   0   0   1 ];        #This is the representation of speech in matrix format using mfcc 
end

[dim ,N]=size(mean_vec_i);
[dim , T]=size(V);
P=cell(N,T);
f=ones(N,T)*(-inf);


t=1;
for i=2:N-1
    P{i,t}=i;
    f(i,t)=log(a_i_j(1,i)) + logDiagGaussian(V(:,t),mean_vec_i(:,i),var_vec_i(:,i));
end
% other f(i,t) terms have been set to -inf


for t=2:T
    for i=2:N-1 
        [f(i,t), argmax] = max( f(1:i,t-1) + log(a_i_j(1:i,i)) );
        %[f(i,t), argmax] = max( f(2:i,t-1) + log(a_i_j(2:i,i)) ); argmax=argmax+1; % if we pass the sub-array of index [2:i] instead of [1:i] to max function
        f(i,t)=f(i,t)+logDiagGaussian(V(:,t),mean_vec_i(:,i),var_vec_i(:,i) );
        P{i,t}=[P{argmax,t-1}  i ];
    end
end

[Fopt,argmax] = max( f(1:N-1,T) + log(a_i_j(1:N-1,N))) ;
%[Fopt,argmax] = max( f(2:N-1,T) + log(a_i_j(2:N-1,N))) ; argmax=argmax+1; % if we pass the sub-array of index [2:N-1] instead of [1:N-1] to max function
if nargout > 1
    varargout(1)= { P{argmax,T} };
end


end
