
class Stock:
    def __init__(self,data:str):
        self.data:str = data
        df = pd.read_csv(data)
        self.df=df.dropna()
        self.data_shape = df.shape
        self.__build_model()
        self.__preprocess()
    def _plot(self):
        plt.figure(figsize=(16,8))
        plt.title('Close Price History')
        plt.plot(self.df['Close'])
        plt.xlabel('Date',fontsize=18)
        plt.ylabel('Close Price USD($)',fontsize=18)
        plt.show()
    def __preprocess(self):
        self.dataf = self.df.filter(['Close'])
        dataset=self.dataf.values
        training_data_len= math.ceil(len(dataset) * .8)

        #scale the data
        scaler=MinMaxScaler(feature_range=(0,1))
        scaled_data=scaler.fit_transform(dataset)
        scaled_data
        train_data=scaled_data[0:training_data_len,:]

        #split the data into x_train and y_train data sets

        x_train =[]
        y_train=[]


        for i in range(60,len(train_data)):
            x_train.append(train_data[i-60:i,0])
            y_train.append(train_data[i,0])
            if i<=60:

            #print(x_train)
            #print(y_train)
                print()
        self.x_train,self.y_train=np.array(x_train),np.array(y_train)
        self.x_train=np.reshape(self.x_train,(self.x_train.shape[0],self.x_train.shape[1],1))
        model=Sequential()
        model.add(LSTM(50,return_sequences=True,input_shape=(self.x_train.shape[1],1)))
        model.add(LSTM(50,return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer='sgd',loss='mean_squared_error')
        model.fit(self.x_train,self.y_train,batch_size=1,epochs=1)
        test_data=scaled_data[training_data_len - 60:,:]
        #create the data sets x_test and y_test
        x_test=[]
        y_test=dataset[training_data_len:,:]
        for i in range(60,len(test_data)):
            x_test.append(test_data[i-60:i,0])
        test_data
        x_test=np.array(x_test)
        x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
        predictions=model.predict(x_test)
        predictions=scaler.inverse_transform(predictions)
        rmse=np.sqrt( np.mean((predictions - y_test)**2))
        train=data[:training_data_len]
        self.valid=data[training_data_len:]
        self.valid['Predictions']=predictions
  
    
    def _plot_predict(self):
        plt.figure(figsize=(16,8))
        plt.title('Model')
        plt.xlabel('Date',fontsize=18)
        plt.ylabel('Close Price USD($)',fontsize=18)
        plt.plot(self.train['Close'])
        plt.plot(self.valid[['Close','Predictions']])
        plt.legend(['Train','Val','Predictions'],loc='lower right')
        plt.show()
        
        
#Test
stock = Stock('ALGO-USD.csv')
stock._plot()
stock._plot_predict()
