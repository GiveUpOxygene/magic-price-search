package java_version;

public class Card {
    public String name;
    public float price;
    public String url;

    public Card(String name, float price, String url) {
        this.name = name;
        this.price = price;
        this.url = url;
    }

    public Card(String name){
        this.name = name;

    }
}