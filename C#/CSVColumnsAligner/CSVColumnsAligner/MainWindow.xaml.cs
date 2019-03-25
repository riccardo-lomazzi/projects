using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace CSVColumnsAligner
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        private string alignedUserInput;


        public string UserInput { get; set; }
        public string AlignedUserInput
        {
            get
            {
                return this.alignedUserInput;
            }
            set
            {
                if (value != this.alignedUserInput)
                {
                    this.alignedUserInput = value;
                    OnPropertyChanged("AlignedUserInput");
                }
            }
        }

        public MainWindow()
        {
            this.UserInput = "";
            this.DataContext = this;
            InitializeComponent();
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            if (this.UserInput.Length == 0)
            {
                this.AlignedUserInput = "Type something";
                return;
            }
            string[] rows = this.UserInput.Split('\r');
            if (rows.Length == 0)
            {
                this.AlignedUserInput = "Type at least two columns";
                return;
            }
            if (rows.Length == 1)
            {
                this.AlignedUserInput = "Type at least two rows";
                return;
            }
            int numberOfColumns = this.GetTotalNumberOfColumns(rows);
            int[] maxNumberOfCharPerColumn = this.GetMaxNumberOfCharsPerColumn(rows, numberOfColumns);
            this.AlignedUserInput = string.Join("\r", this.AlignUserInput(rows, maxNumberOfCharPerColumn));
        }

        private int GetTotalNumberOfColumns(string[] rows)
        {
            int numberOfColumns = 0;
            foreach (string row in rows)
            {
                string[] rowColumns = row.Split(',');
                if (rowColumns.Length > numberOfColumns)
                    numberOfColumns = rowColumns.Length;
            }
            return numberOfColumns;
        }

        private int[] GetMaxNumberOfCharsPerColumn(string[] rows, int numberOfColumns)
        {
            int[] counters = new int[numberOfColumns];
            //initialize counters
            for (int i = 0; i < counters.Length; i++)
            {
                counters[i] = 0;
            }
            foreach (string row in rows)
            {
                string[] rowColumns = row.Split(',');
                int j = 0;
                foreach (string column in rowColumns)
                {
                    if (j < rowColumns.Length && counters[j] < column.Length)
                    {
                        counters[j] = column.Length;
                    }
                    j++;
                }
            }
            return counters;
        }

        private string[] AlignUserInput(string[] rows, int[] maxNumberOfCharPerColumn)
        {
            for (int i = 0; i < rows.Length; i++)
            {
                string[] rowColumns = rows[i].Split(',');
                int mnocpcIndex = 0;
                for (int j = 0; j < rowColumns.Length; j++)
                {
                    int spacesToAdd = maxNumberOfCharPerColumn[mnocpcIndex] - rowColumns[j].Length;
                    if (mnocpcIndex < rowColumns.Length && spacesToAdd > 0)
                    {
                        while (spacesToAdd > 0)
                        {
                            rowColumns[j] += ' ';
                            spacesToAdd--;
                        }
                    }
                    mnocpcIndex++;
                }
                rows[i] = string.Join(",", rowColumns);
            }
            return rows;
        }
    }
}
